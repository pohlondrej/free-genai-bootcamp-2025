package com.pohlondrej.langportal.backend

import io.ktor.client.request.get
import io.ktor.client.statement.bodyAsText
import io.ktor.http.HttpStatusCode
import io.ktor.server.config.MapApplicationConfig
import io.ktor.server.testing.TestApplicationBuilder
import io.ktor.server.testing.testApplication
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNotNull

class ApplicationTest {

    private fun TestApplicationBuilder.configureTestApplication() {
        environment {
            config = MapApplicationConfig(
                "ktor.database.file" to "words.db"
            )
        }
        application {
            module()
        }
    }

    @Test
    fun testWords() = testApplication {
        configureTestApplication()
        client.get("/api/words").apply {
            assertEquals(HttpStatusCode.OK, status)
            assertNotNull(bodyAsText())
        }
    }

    @Test
    fun testWordById() = testApplication {
        configureTestApplication()
        client.get("/api/words/1").apply { // Assuming word with ID 1 exists
            assertEquals(HttpStatusCode.OK, status)
            assertNotNull(bodyAsText())
        }
    }

    @Test
    fun testGroups() = testApplication {
        configureTestApplication()
        client.get("/api/groups").apply {
            assertEquals(HttpStatusCode.OK, status)
            assertNotNull(bodyAsText())
        }
    }

    @Test
    fun testGroupById() = testApplication {
        configureTestApplication()
        client.get("/api/groups/1").apply { // Assuming group with ID 1 exists
            assertEquals(HttpStatusCode.OK, status)
            assertNotNull(bodyAsText())
        }
    }

    @Test
    fun testGroupWords() = testApplication {
        configureTestApplication()
        client.get("/api/groups/1/words").apply { // Assuming group with ID 1 exists
            assertEquals(HttpStatusCode.OK, status)
            assertNotNull(bodyAsText())
        }
    }

    @Test
    fun testGroupStudySessions() = testApplication {
        configureTestApplication()
        client.get("/api/groups/1/study_sessions").apply { // Assuming group with ID 1 exists
            assertEquals(HttpStatusCode.OK, status)
            assertNotNull(bodyAsText())
        }
    }

    @Test
    fun testDashboardLastStudySession() = testApplication {
        configureTestApplication()
        client.get("/api/dashboard/last_study_session").apply {
            assertEquals(HttpStatusCode.OK, status)
            assertNotNull(bodyAsText())
        }
    }

    @Test
    fun testDashboardStudyProgress() = testApplication {
        configureTestApplication()
        client.get("/api/dashboard/study_progress").apply {
            assertEquals(HttpStatusCode.OK, status)
            assertNotNull(bodyAsText())
        }
    }

    @Test
    fun testDashboardQuickStats() = testApplication {
        configureTestApplication()
        client.get("/api/dashboard/quick_stats").apply {
            assertEquals(HttpStatusCode.OK, status)
            assertNotNull(bodyAsText())
        }
    }

    @Test
    fun testStudyActivities() = testApplication {
        configureTestApplication()
        client.get("/api/study_activities").apply {
            assertEquals(HttpStatusCode.OK, status)
            assertNotNull(bodyAsText())
        }
    }

    @Test
    fun testStudyActivityById() = testApplication {
        configureTestApplication()
        client.get("/api/study_activities/1").apply { // Assuming study activity with ID 1 exists
            assertEquals(HttpStatusCode.OK, status)
            assertNotNull(bodyAsText())
        }
    }

    @Test
    fun testStudyActivityStudySessions() = testApplication {
        configureTestApplication()
        client.get("/api/study_activities/1/study_sessions").apply { // Assuming study activity with ID 1 exists
            assertEquals(HttpStatusCode.OK, status)
            assertNotNull(bodyAsText())
        }
    }

    @Test
    fun testStudySessions() = testApplication {
        configureTestApplication()
        client.get("/api/study_sessions").apply {
            assertEquals(HttpStatusCode.OK, status)
            assertNotNull(bodyAsText())
        }
    }

    @Test
    fun testStudySessionById() = testApplication {
        configureTestApplication()
        client.get("/api/study_sessions/1").apply { // Assuming study session with ID 1 exists
            assertEquals(HttpStatusCode.OK, status)
            assertNotNull(bodyAsText())
        }
    }

    @Test
    fun testStudySessionWords() = testApplication {
        configureTestApplication()
        client.get("/api/study_sessions/1/words").apply { // Assuming study session with ID 1 exists
            assertEquals(HttpStatusCode.OK, status)
            assertNotNull(bodyAsText())
        }
    }

    @Test
    fun testSettings() = testApplication {
        configureTestApplication()
        client.get("/api/settings").apply {
            assertEquals(HttpStatusCode.OK, status)
            assertNotNull(bodyAsText())
        }
    }
}
