package com.pohlondrej.langportal.backend

import com.pohlondrej.langportal.backend.data.createStudyActivity
import com.pohlondrej.langportal.backend.data.fullReset
import com.pohlondrej.langportal.backend.data.getGroup
import com.pohlondrej.langportal.backend.data.getGroupStudySessions
import com.pohlondrej.langportal.backend.data.getGroupWords
import com.pohlondrej.langportal.backend.data.getGroups
import com.pohlondrej.langportal.backend.data.getLastStudySession
import com.pohlondrej.langportal.backend.data.getQuickStats
import com.pohlondrej.langportal.backend.data.getSettings
import com.pohlondrej.langportal.backend.data.getStudyActivities
import com.pohlondrej.langportal.backend.data.getStudyActivity
import com.pohlondrej.langportal.backend.data.getStudyProgress
import com.pohlondrej.langportal.backend.data.getStudySession
import com.pohlondrej.langportal.backend.data.getStudySessionWords
import com.pohlondrej.langportal.backend.data.getStudySessions
import com.pohlondrej.langportal.backend.data.getWord
import com.pohlondrej.langportal.backend.data.getWords
import com.pohlondrej.langportal.backend.data.requests.CreateStudyActivityRequest
import com.pohlondrej.langportal.backend.data.requests.ReviewWordRequest
import com.pohlondrej.langportal.backend.data.resetHistory
import com.pohlondrej.langportal.backend.data.responses.PaginatedResponse
import com.pohlondrej.langportal.backend.data.reviewWord
import io.ktor.http.HttpStatusCode
import io.ktor.server.application.Application
import io.ktor.server.request.receive
import io.ktor.server.request.receiveParameters
import io.ktor.server.response.respondText
import io.ktor.server.response.respond
import io.ktor.server.routing.routing
import io.ktor.server.routing.get
import io.ktor.server.routing.post

fun Application.configureRouting() {
    routing {
        get("/") {
            call.respondText("Hello World!")
        }

        get("/api/words") {
            val page = call.parameters["page"]?.toIntOrNull() ?: 1
            val (words, pagination) = getWords(page)
            val response = PaginatedResponse(words, pagination)
            call.respond(response)
        }

        get("/api/words/{id}") {
            val id = call.parameters["id"]?.toIntOrNull()
            if (id == null) {
                call.respond(HttpStatusCode.BadRequest, "Invalid ID")
                return@get
            }

            val word = getWord(id)
            if (word == null) {
                call.respond(HttpStatusCode.NotFound, "Word not found")
                return@get
            }

            call.respond(word)
        }

        get("/api/groups") {
            val page = call.parameters["page"]?.toIntOrNull() ?: 1
            val (groups, pagination) = getGroups(page)
            call.respond(PaginatedResponse(groups, pagination))
        }

        get("/api/groups/{id}") {
            val id = call.parameters["id"]?.toIntOrNull()
            if (id == null) {
                call.respond(HttpStatusCode.BadRequest, "Invalid ID")
                return@get
            }

            val group = getGroup(id)
            if (group == null) {
                call.respond(HttpStatusCode.NotFound, "Group not found")
                return@get
            }

            call.respond(group)
        }

        get("/api/groups/{id}/words") {
            val id = call.parameters["id"]?.toIntOrNull()
            if (id == null) {
                call.respond(HttpStatusCode.BadRequest, "Invalid ID")
                return@get
            }

            val page = call.parameters["page"]?.toIntOrNull() ?: 1
            val (words, pagination) = getGroupWords(id, page)
            call.respond(PaginatedResponse(words, pagination))
        }

        get("/api/groups/{id}/study_sessions") {
            val id = call.parameters["id"]?.toIntOrNull()
            if (id == null) {
                call.respond(HttpStatusCode.BadRequest, "Invalid ID")
                return@get
            }

            val page = call.parameters["page"]?.toIntOrNull() ?: 1
            val (sessions, pagination) = getGroupStudySessions(id, page)
            call.respond(PaginatedResponse(sessions, pagination))
        }

        get("/api/dashboard/last_study_session") {
            val session = getLastStudySession()
            if (session == null) {
                call.respond(HttpStatusCode.NotFound, "No study sessions found")
                return@get
            }
            call.respond(session)
        }

        get("/api/dashboard/study_progress") {
            call.respond(getStudyProgress())
        }

        get("/api/dashboard/quick_stats") {
            call.respond(getQuickStats())
        }

        get("/api/study_activities") {
            call.respond(getStudyActivities())
        }

        get("/api/study_activities/{id}") {
            val id = call.parameters["id"]?.toIntOrNull()
            if (id == null) {
                call.respond(HttpStatusCode.BadRequest, "Invalid ID")
                return@get
            }

            val activity = getStudyActivity(id)
            if (activity == null) {
                call.respond(HttpStatusCode.NotFound, "Study activity not found")
                return@get
            }

            call.respond(activity)
        }

        get("/api/study_activities/{id}/study_sessions") {
            val id = call.parameters["id"]?.toIntOrNull()
            if (id == null) {
                call.respond(HttpStatusCode.BadRequest, "Invalid ID")
                return@get
            }

            val page = call.parameters["page"]?.toIntOrNull() ?: 1
            val (sessions, pagination) = getGroupStudySessions(id, page)
            call.respond(PaginatedResponse(sessions, pagination))
        }

        get("/api/study_sessions") {
            val page = call.parameters["page"]?.toIntOrNull() ?: 1
            val (sessions, pagination) = getStudySessions(page)
            call.respond(PaginatedResponse(sessions, pagination))
        }

        get("/api/study_sessions/{id}") {
            val id = call.parameters["id"]?.toIntOrNull()
            if (id == null) {
                call.respond(HttpStatusCode.BadRequest, "Invalid ID")
                return@get
            }

            val session = getStudySession(id)
            if (session == null) {
                call.respond(HttpStatusCode.NotFound, "Study session not found")
                return@get
            }

            call.respond(session)
        }

        get("/api/study_sessions/{id}/words") {
            val id = call.parameters["id"]?.toIntOrNull()
            if (id == null) {
                call.respond(HttpStatusCode.BadRequest, "Invalid ID")
                return@get
            }

            val page = call.parameters["page"]?.toIntOrNull() ?: 1
            val (words, pagination) = getStudySessionWords(id, page)
            call.respond(PaginatedResponse(words, pagination))
        }

        get("/api/settings") {
            call.respond(getSettings())
        }

        post("/api/study_activities") {
            try {
                val request = call.receive<CreateStudyActivityRequest>()
                call.respond(createStudyActivity(request.groupId, request.studyActivityId))
            } catch (e: Exception) { // Catch potential ContentNegotiationException
                call.respond(HttpStatusCode.BadRequest, "Invalid request body format. Expected JSON.")
            }
        }

        post("/api/reset_history") {
            call.respond(resetHistory())
        }

        post("/api/full_reset") {
            call.respond(fullReset())
        }

        post("/api/study_sessions/{id}/words/{word_id}/review") {
            val sessionId = call.parameters["id"]?.toIntOrNull()
            val wordId = call.parameters["word_id"]?.toIntOrNull()

            if (sessionId == null || wordId == null) {
                call.respond(HttpStatusCode.BadRequest, "Invalid session ID or word ID")
                return@post
            }

            try {
                val request = call.receive<ReviewWordRequest>()
                val correct = request.correct

                call.respond(reviewWord(sessionId, wordId, correct))
            } catch (e: Exception) {
                call.respond(
                    HttpStatusCode.BadRequest,
                    "Invalid request body format. Expected JSON with 'correct' parameter."
                )
            }
        }
    }
}
