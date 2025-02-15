package com.pohlondrej.langportal.backend

import io.ktor.server.application.Application
import io.ktor.server.netty.EngineMain

fun main(args: Array<String>) {
    EngineMain.main(args)
}

fun Application.module() {
    configureDatabase()
    configureHTTP()
    configureSerialization()
    configureFrameworks()
    configureRouting()
}
