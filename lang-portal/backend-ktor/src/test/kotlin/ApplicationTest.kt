package com.pohlondrej.langportal.backend

import io.ktor.client.request.get
import io.ktor.http.HttpStatusCode
import io.ktor.server.config.MapApplicationConfig
import io.ktor.server.testing.testApplication
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class ApplicationTest {

    @Test
    fun testWords() = testApplication {
        environment {
            config = MapApplicationConfig(
                "ktor.database.file" to "words.db"
            )
        }
        application {
            module()
        }
        client.get("/api/words").apply {
            assertTrue(true)
            assertEquals(HttpStatusCode.OK, status)
        }
    }

}
