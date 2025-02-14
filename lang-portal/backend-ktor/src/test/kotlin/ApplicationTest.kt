package com.pohlondrej.langportal.backend

import io.ktor.client.call.body
import io.ktor.client.request.*
import io.ktor.client.utils.EmptyContent.contentType
import io.ktor.http.ContentType
import io.ktor.http.HttpStatusCode
import io.ktor.http.contentType
import io.ktor.server.testing.testApplication
import io.ktor.utils.io.InternalAPI
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNotNull

class ApplicationTest {

    @Test
    fun testRoot() = testApplication {
        application { module() }
        client.get("/").apply {
            assertEquals(HttpStatusCode.OK, status)
        }
    }
    
    @Test
    fun testListWords() = testApplication {
        application { module() }
        client.get("/words").apply {
            assertEquals(HttpStatusCode.OK, status)
            // Additional assertions can be added to check the response body
        }
    }
    
    @Test
    fun testGetWordDetails() = testApplication {
        application { module() }
        client.get("/words/1").apply {
            assertEquals(HttpStatusCode.OK, status)
            // Additional assertions can be added to check the response body
        }
    }
    
    @Test
    fun testListGroups() = testApplication {
        application { module() }
        client.get("/groups").apply {
            assertEquals(HttpStatusCode.OK, status)
            // Additional assertions can be added to check the response body
        }
    }
    
    @Test
    fun testGetGroupDetails() = testApplication {
        application { module() }
        client.get("/groups/1").apply {
            assertEquals(HttpStatusCode.OK, status)
            // Additional assertions can be added to check the response body
        }
    }
    
    @Test
    fun testListStudySessions() = testApplication {
        application { module() }
        client.get("/study-sessions").apply {
            assertEquals(HttpStatusCode.OK, status)
            // Additional assertions can be added to check the response body
        }
    }
    
    @Test
    fun testGetStudySessionDetails() = testApplication {
        application { module() }
        client.get("/study-sessions/1").apply {
            assertEquals(HttpStatusCode.OK, status)
            // Additional assertions can be added to check the response body
        }
    }
    
    @Test
    fun testListStudyActivities() = testApplication {
        application { module() }
        client.get("/study-activities").apply {
            assertEquals(HttpStatusCode.OK, status)
            // Additional assertions can be added to check the response body
        }
    }
    
    @Test
    fun testGetStudyActivityDetails() = testApplication {
        application { module() }
        client.get("/study-activities/1").apply {
            assertEquals(HttpStatusCode.OK, status)
            // Additional assertions can be added to check the response body
        }
    }
    
    @OptIn(InternalAPI::class)
    @Test
    fun testCreateWord() = testApplication {
        application { module() }
        val newWord = mapOf(
            "japanese" to "ありがとう",
            "romaji" to "arigatou",
            "english" to "thank you"
        )
        val response = client.post("/words") {
            contentType(ContentType.Application.Json)
            body = newWord
        }
        assertEquals(HttpStatusCode.Created, response.status)
        val responseBody = response.body<String>()
        assertNotNull(responseBody)
        // Additional assertions can be added to check the response body
    }
}
