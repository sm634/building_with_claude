financial_analysis_schema = {
    "name": "analyze_financial_statement",
    "description": "Analyzes a financial statements to provides insights.",
    "input_schema": {
        "type": "object",
        "properties": {
            "balance": {
                "type": "integer",
                "description": "The current balance..."
            },
        "key_insights": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "A list of key insights derived from the financial statement."
            },
        },
    }
}

