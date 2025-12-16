# Nombre del Archivo: dashboard_repository.py
# Descripción: Repositorio de dashboards - Operaciones CRUD para dashboards persistentes en base de datos
# Autor: Fernando Bavera Villalba
# Fecha: 25/10/2025

import json
import logging
import streamlit as st
from datetime import datetime
from typing import Any, Dict, List, Optional

from core.database import db_manager

logger = logging.getLogger(__name__)

# Utilidad - Convertir Fila a Diccionario
def _row_to_dict(row: Any) -> Dict[str, Any]:
    """Convertir fila de SQLite Row o psycopg2 a diccionario plano."""
    if row is None:
        return {}
    if isinstance(row, dict):
        return row
    try:
        return dict(row)
    except Exception:
        return row


# Base de Datos - Crear o Actualizar Dashboard
def upsert_dashboard(
    user_id: int,
    dashboard_name: str,
    components: List[Dict[str, Any]],
    dashboard_id: Optional[int] = None,
    is_public: bool = False,
    dataset_info: Optional[Dict[str, Any]] = None,
) -> int:
    """
    Crear o actualizar un registro de dashboard en la base de datos persistente.

    Args:
        user_id: Propietario del dashboard.
        dashboard_name: Nombre amigable para humanos.
        components: Lista de componentes del dashboard (serialización de session-state).
        dashboard_id: ID de dashboard existente (actualiza cuando se proporciona).
        is_public: Bandera de visibilidad (uso futuro).

    Returns:
        El ID del dashboard persistido.
    """
    if not user_id:
        raise ValueError("user_id is required to persist a dashboard.")

    if not components:
        raise ValueError("Cannot persist an empty dashboard.")

    # Timestamp - Obtener timestamp actual
    now = datetime.utcnow().isoformat()
    config_payload = {
        "version": "1.0",
        "saved_at": now,
        "components": components,
    }
    if dataset_info:
        config_payload["dataset_info"] = dataset_info
    # Conversion - Convertir configuración a JSON
    dashboard_config = json.dumps(config_payload, ensure_ascii=False)

    with db_manager.get_connection() as conn:
        if dashboard_id:
            # Actualizacion - Actualizar dashboard existente
            logger.debug("Updating dashboard id %s for user %s", dashboard_id, user_id)
            conn.execute(
                """
                UPDATE dashboards
                SET dashboard_name = ?, dashboard_config = ?, is_public = ?,
                    updated_at = ?, last_accessed = ?
                WHERE id = ? AND user_id = ?
                """,
                (dashboard_name, dashboard_config, is_public, now, now, dashboard_id, user_id),
            )
            conn.commit()
            
            # Cache - Invalidar caché para asegurar datos frescos en la próxima llamada
            list_user_dashboards.clear()
            
            return dashboard_id

        # Creacion - Crear nuevo dashboard
        logger.debug("Creating new dashboard for user %s", user_id)
        if db_manager.db_type == "supabase":
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO dashboards (
                    user_id, dashboard_name, dashboard_config, is_public,
                    created_at, updated_at, last_accessed
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                RETURNING id
                """,
                (user_id, dashboard_name, dashboard_config, is_public, now, now, now),
            )
            record = cursor.fetchone()
            conn.commit()
            
            # Cache - Invalidar caché para asegurar datos frescos en la próxima llamada
            list_user_dashboards.clear()
            
            return record["id"] if record else dashboard_id or 0

        cursor = conn.execute(
            """
            INSERT INTO dashboards (
                user_id, dashboard_name, dashboard_config, is_public,
                created_at, updated_at, last_accessed
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, dashboard_name, dashboard_config, is_public, now, now, now),
        )
        conn.commit()
        
        # Cache - Invalidar caché para asegurar datos frescos en la próxima llamada
        list_user_dashboards.clear()
        
        return int(cursor.lastrowid)


# Consulta - Listar Dashboards del Usuario
@st.cache_data(show_spinner=False, ttl=30)
def list_user_dashboards(user_id: int) -> List[Dict[str, Any]]:
    """Recuperar todos los dashboards de un usuario ordenados por última actualización.
    
    Cacheados por 30 segundos para reducir consultas a la base de datos mientras se permiten
    actualizaciones en tiempo real cuando se crean/modifican dashboards.
    """
    if not user_id:
        return []

    with db_manager.get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT id, dashboard_name, dashboard_config,
                   created_at, updated_at, last_accessed, is_public
            FROM dashboards
            WHERE user_id = ?
            ORDER BY updated_at DESC, created_at DESC
            """,
            (user_id,),
        )
        rows = cursor.fetchall()

    dashboards: List[Dict[str, Any]] = []
    for row in rows:
        record = _row_to_dict(row)
        config_raw = record.get("dashboard_config", "{}")
        try:
            # Conversion - Parsear configuración JSON
            parsed_config = json.loads(config_raw) if isinstance(config_raw, str) else config_raw
        except json.JSONDecodeError:
            # Manejo de Errores - Usar configuración por defecto si falla el parseo
            parsed_config = {"components": []}

        dashboards.append(
            {
                "id": record.get("id"),
                "dashboard_name": record.get("dashboard_name", "Dashboard sin nombre"),
                "config": parsed_config,
                "created_at": record.get("created_at"),
                "updated_at": record.get("updated_at"),
                "last_accessed": record.get("last_accessed"),
                "is_public": record.get("is_public", False),
                "dataset_info": parsed_config.get("dataset_info", {}),
            }
        )
    return dashboards


# Base de Datos - Eliminar Dashboard
def delete_dashboard(dashboard_id: int, user_id: int) -> None:
    """Eliminar un dashboard que pertenece al usuario proporcionado."""
    if not dashboard_id or not user_id:
        return

    with db_manager.get_connection() as conn:
        conn.execute(
            "DELETE FROM dashboards WHERE id = ? AND user_id = ?",
            (dashboard_id, user_id),
        )
        conn.commit()
    
    # Cache - Invalidar Cache para Asegurar Datos Frescos
    list_user_dashboards.clear()

