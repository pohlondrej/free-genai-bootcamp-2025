package com.pohlondrej.langportal.backend

import com.pohlondrej.langportal.backend.database.DatabaseFactory
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*

fun main(args: Array<String>): Unit = EngineMain.main(args)

fun Application.module() {
    DatabaseFactory.init()
    configureRouting()
    configureSerialization()
    configureHTTP()
    configureFrameworks()
}
