def load_level_styles():
    """Load the CSS styling for level pages"""
    return """
    <style>
    /* ===== Global Styles ===== */
    body {
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
        line-height: 1.6;
        color: var(--text-color);
        background-color: var(--background-color);
        margin: 0;
        padding: 0;
    }

    /* Headings */
    h1, h2, h3, h4, h5 {
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: var(--text-color);
    }

    /* Paragraphs and text */
    p {
        margin-bottom: 1rem;
        color: var(--text-color);
    }

    /* ===== Separator Styles ===== */
    .separator-thin {
        margin: 1rem 0;
        border: none;
        height: 2px;
        background: var(--text-color);
        opacity: 0.3;
        border-radius: 1px;
    }

    .separator-gradient {
        margin: 1rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--text-color), transparent);
        opacity: 0.3;
        border-radius: 1px;
    }

    .separator-colorful {
        margin: 1rem 0;
        border: none;
        height: 3px;
        background: linear-gradient(90deg, #ff6b6b, #4facfe);
        border-radius: 2px;
    }

    .separator-dotted {
        margin: 1rem 0;
        border: none;
        height: 2px;
        background: repeating-linear-gradient(
            90deg,
            var(--text-color) 0px,
            var(--text-color) 4px,
            transparent 4px,
            transparent 12px
        );
        opacity: 0.3;
        border-radius: 1px;
    }

    /* ===== Containers ===== */
    .section {
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
        background-color: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }

    /* Cards */
    .card {
        border-radius: 12px;
        padding: 1rem;
        background-color: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    /* Lists */
    ul, ol {
        margin-left: 1.5rem;
        margin-bottom: 1rem;
        color: var(--text-color);
    }

    li {
        color: var(--text-color);
    }

    /* Emojis inline with text */
    .emoji {
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }

    /* ===== Responsive ===== */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.75rem;
        }
        h2 {
            font-size: 1.5rem;
        }
        .section {
            padding: 1rem;
        }
    }

    /* Custom progress bar styling */
    .progress-container {
        background-color: rgba(128, 128, 128, 0.1);
        border: 1px solid rgba(128, 128, 128, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }

    /* Step cards */
    .step-card {
        background-color: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .step-card h3,
    .step-card h4,
    .step-card p,
    .step-card ul,
    .step-card ol,
    .step-card li {
        color: var(--text-color) !important;
    }

    .step-number {
        background: linear-gradient(135deg, #4facfe, #00f2fe);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }

    /* Info boxes */
    .info-box {
        background-color: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .info-box h3,
    .info-box p,
    .info-box ul,
    .info-box ol,
    .info-box li {
        color: var(--text-color) !important;
    }

    .warning-box {
        background-color: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .warning-box h3,
    .warning-box p,
    .warning-box ul,
    .warning-box ol,
    .warning-box li {
        color: var(--text-color) !important;
    }

    .success-box {
        background-color: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .success-box h3,
    .success-box p,
    .success-box ul,
    .success-box ol,
    .success-box li {
        color: var(--text-color) !important;
    }

    /* Ensure all text in cards is readable */
    .card h3,
    .card p,
    .card ul,
    .card ol,
    .card li {
        color: var(--text-color) !important;
    }

    /* Dark mode specific adjustments */
    @media (prefers-color-scheme: dark) {
        .step-card,
        .card,
        .section {
            background-color: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.2);
        }
        
        .progress-container {
            background-color: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.3);
        }
    }

    /* Light mode specific adjustments */
    @media (prefers-color-scheme: light) {
        .step-card,
        .card,
        .section {
            background-color: rgba(0, 0, 0, 0.05);
            border-color: rgba(0, 0, 0, 0.2);
        }
        
        .progress-container {
            background-color: rgba(0, 0, 0, 0.1);
            border-color: rgba(0, 0, 0, 0.3);
        }
    }

    /* ===== Progression and Achievement Styles ===== */
    .progression-summary {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.1), rgba(0, 242, 254, 0.1));
        border: 1px solid rgba(79, 172, 254, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .progress-stats {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
        flex-wrap: wrap;
    }

    .stat-item {
        text-align: center;
        margin: 0.5rem;
    }

    .stat-number {
        display: block;
        font-size: 2rem;
        font-weight: bold;
        color: #4facfe;
        margin-bottom: 0.25rem;
    }

    .stat-label {
        font-size: 0.9rem;
        color: var(--text-color);
        opacity: 0.8;
    }

    .achievements-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }

    .achievement-badge {
        background-color: rgba(255, 255, 255, 0.1);
        border: 2px solid;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        transition: transform 0.2s ease;
    }

    .achievement-badge:hover {
        transform: translateY(-2px);
    }

    .badge-icon {
        font-size: 2rem;
        display: block;
        margin-bottom: 0.5rem;
    }

    .badge-title {
        font-size: 0.9rem;
        font-weight: bold;
        color: var(--text-color);
    }

    .achievement-card {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .achievement-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }

    .achievement-icon {
        font-size: 2rem;
        margin-right: 1rem;
    }

    .next-milestone {
        background-color: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
    }

    .data-quality-card {
        background-color: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .quality-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .quality-score {
        font-size: 1.2rem;
        font-weight: bold;
    }

    .quality-details {
        font-size: 0.9rem;
        opacity: 0.8;
        margin-top: 0.5rem;
    }

    .level-preview {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(79, 172, 254, 0.1));
        border: 1px solid rgba(255, 107, 107, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .preview-content {
        margin-top: 1rem;
    }

    .preview-next {
        background-color: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 6px;
        padding: 0.75rem;
        margin-top: 1rem;
    }

    /* Responsive adjustments for progression elements */
    @media (max-width: 768px) {
        .progress-stats {
            flex-direction: column;
            align-items: center;
        }
        
        .achievements-grid {
            grid-template-columns: 1fr;
        }
        
        .achievement-header {
            flex-direction: column;
            text-align: center;
        }
        
        .achievement-icon {
            margin-right: 0;
            margin-bottom: 0.5rem;
        }
    }
    </style>
    """
