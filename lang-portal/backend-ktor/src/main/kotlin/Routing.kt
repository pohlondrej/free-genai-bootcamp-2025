package com.example

import io.ktor.server.application.Application
import io.ktor.server.response.respondText
import io.ktor.server.routing.routing
import io.ktor.server.routing.get
import io.ktor.server.routing.post

fun Application.configureRouting() {
    routing {
        get("/") {
            call.respondText("Hello World!")
        }

        get("/api/words") {
            // Handle fetching words with pagination (default 100 items per page)
        }

        get("/api/words/{id}") {
            // Handle fetching a word by ID
        }

        get("/api/groups") {
            // Handle fetching groups with pagination (default 100 items per page)
        }

        get("/api/groups/{id}") {
            // Handle fetching a group by ID
        }

        get("/api/groups/{id}/words") {
            // Handle fetching words associated with a group, with pagination
        }

        get("/api/dashboard/last_study_session") {
            // Handle fetching data for the last study session
        }

        get("/api/dashboard/study_progress") {
            // Handle fetching study progress
        }

        get("/api/dashboard/quick_stats") {
            // Handle fetching quick stats for the dashboard
        }

        get("/api/study_activities") {
            // Handle fetching study activities
        }

        get("/api/study_activities/{id}") {
            // Handle fetching a specific study activity
        }

        get("/api/study_activities/{id}/study_sessions") {
            // Handle fetching study sessions related to a specific study activity
        }

        post("/api/study_activities") {
            // Handle creating a new study activity
        }

        get("/api/study_sessions") {
            // Handle fetching study sessions with pagination
        }

        get("/api/study_sessions/{id}") {
            // Handle fetching a specific study session
        }

        get("/api/study_sessions/{id}/words") {
            // Handle fetching words for a specific study session
        }

        get("/api/settings") {
            // Handle fetching app settings
        }

        post("/api/reset_history") {
            // Handle resetting user history
        }

        post("/api/full_reset") {
            // Handle fully resetting user data
        }

        post("/api/study_sessions/{id}/words/{word_id}/review") {
            // Handle reviewing a word in a specific study session
        }
    }
}
