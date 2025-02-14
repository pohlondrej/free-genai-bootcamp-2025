package com.pohlondrej.langportal.backend.config

data class AppConfig(
    val isDevelopment: Boolean,
    val databasePath: String
) {
    companion object {
        fun fromEnvironment(isDevelopment: Boolean): AppConfig {
            val dbName = if (isDevelopment) "data_dev.db" else "data.db"
            return AppConfig(
                isDevelopment = isDevelopment,
                databasePath = dbName
            )
        }
    }
}
