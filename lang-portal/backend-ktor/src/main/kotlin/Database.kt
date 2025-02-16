package com.pohlondrej.langportal.backend

import io.ktor.server.application.Application
import org.jetbrains.exposed.sql.Database

fun Application.configureDatabase() {
    val dbFile = environment.config.property("ktor.database.file").getString()
    val dbPath = "jdbc:sqlite:$dbFile"
    Database.connect(dbPath, "org.sqlite.JDBC")
}