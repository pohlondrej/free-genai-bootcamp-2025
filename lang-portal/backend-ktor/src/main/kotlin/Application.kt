package com.pohlondrej.langportal.backend

import io.ktor.http.HttpHeaders
import io.ktor.server.application.Application
import io.ktor.server.netty.EngineMain
import io.ktor.server.application.install
import io.ktor.server.plugins.cors.routing.CORS

fun main(args: Array<String>) {
    EngineMain.main(args)
}

fun Application.module() {
    install(CORS) {
        anyHost()
        allowHeader(HttpHeaders.ContentType)
    }
    configureDatabase()
    configureHTTP()
    configureSerialization()
    configureFrameworks()
    configureRouting()
}
