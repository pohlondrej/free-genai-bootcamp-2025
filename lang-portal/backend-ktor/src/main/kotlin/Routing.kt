package com.pohlondrej.langportal.backend

import com.pohlondrej.langportal.backend.data.PaginatedResponse
import com.pohlondrej.langportal.backend.service.DatabaseService
import io.ktor.http.*
import io.ktor.server.request.*
import io.ktor.server.application.Application
import io.ktor.server.response.respond
import io.ktor.server.response.respondText
import io.ktor.server.routing.routing
import io.ktor.server.routing.get
import io.ktor.server.routing.post


fun Application.configureRouting() {
    val databaseService = DatabaseService()

    routing {
        get("/") {
            call.respondText("Hello World!")
        }

        get("/api/words") {
            val page = call.parameters["page"]?.toIntOrNull() ?: 1
            val (words, pagination) = databaseService.getWords(page)
            call.respond(PaginatedResponse(words, pagination))
        }

        get("/api/words/{id}") {
            val id = call.parameters["id"]?.toIntOrNull()
            if (id == null) {
                call.respond(HttpStatusCode.BadRequest, "Invalid ID")
                return@get
            }

            val word = databaseService.getWord(id)
            if (word == null) {
                call.respond(HttpStatusCode.NotFound, "Word not found")
                return@get
            }

            call.respond(word)
        }

        get("/api/groups") {
            val page = call.parameters["page"]?.toIntOrNull() ?: 1
            val (groups, pagination) = databaseService.getGroups(page)
            call.respond(PaginatedResponse(groups, pagination))
        }

        get("/api/groups/{id}") {
            val id = call.parameters["id"]?.toIntOrNull()
            if (id == null) {
                call.respond(HttpStatusCode.BadRequest, "Invalid ID")
                return@get
            }

            val group = databaseService.getGroup(id)
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
            val (words, pagination) = databaseService.getGroupWords(id, page)
            call.respond(PaginatedResponse(words, pagination))
        }

        get("/api/groups/{id}/study_sessions") {
            val id = call.parameters["id"]?.toIntOrNull()
            if (id == null) {
                call.respond(HttpStatusCode.BadRequest, "Invalid ID")
                return@get
            }

            val page = call.parameters["page"]?.toIntOrNull() ?: 1
            val (sessions, pagination) = databaseService.getGroupStudySessions(id, page)
            call.respond(PaginatedResponse(sessions, pagination))
        }

        get("/api/dashboard/last_study_session") {
            val session = databaseService.getLastStudySession()
            if (session == null) {
                call.respond(HttpStatusCode.NotFound, "No study sessions found")
                return@get
            }
            call.respond(session)
        }

        get("/api/dashboard/study_progress") {
            call.respond(databaseService.getStudyProgress())
        }

        get("/api/dashboard/quick_stats") {
            call.respond(databaseService.getQuickStats())
        }

        get("/api/study_activities") {
            call.respond(databaseService.getStudyActivities())
        }

        get("/api/study_activities/{id}") {
            val id = call.parameters["id"]?.toIntOrNull()
            if (id == null) {
                call.respond(HttpStatusCode.BadRequest, "Invalid ID")
                return@get
            }

            val activity = databaseService.getStudyActivity(id)
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
            val (sessions, pagination) = databaseService.getGroupStudySessions(id, page)
            call.respond(PaginatedResponse(sessions, pagination))
        }

        get("/api/study_sessions") {
            val page = call.parameters["page"]?.toIntOrNull() ?: 1
            val (sessions, pagination) = databaseService.getStudySessions(page)
            call.respond(PaginatedResponse(sessions, pagination))
        }

        get("/api/study_sessions/{id}") {
            val id = call.parameters["id"]?.toIntOrNull()
            if (id == null) {
                call.respond(HttpStatusCode.BadRequest, "Invalid ID")
                return@get
            }

            val session = databaseService.getStudySession(id)
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
            val (words, pagination) = databaseService.getStudySessionWords(id, page)
            call.respond(PaginatedResponse(words, pagination))
        }

        get("/api/settings") {
            call.respond(databaseService.getSettings())
        }

        post("/api/study_activities") {
            val parameters = call.receiveParameters()
            val groupId = parameters["group_id"]?.toIntOrNull()
            val studyActivityId = parameters["study_activity_id"]?.toIntOrNull()

            if (groupId == null || studyActivityId == null) {
                call.respond(HttpStatusCode.BadRequest, "Missing or invalid parameters")
                return@post
            }

            call.respond(databaseService.createStudyActivity(groupId, studyActivityId))
        }

        post("/api/reset_history") {
            call.respond(databaseService.resetHistory())
        }

        post("/api/full_reset") {
            call.respond(databaseService.fullReset())
        }

        post("/api/study_sessions/{id}/words/{word_id}/review") {
            val sessionId = call.parameters["id"]?.toIntOrNull()
            val wordId = call.parameters["word_id"]?.toIntOrNull()
            
            if (sessionId == null || wordId == null) {
                call.respond(HttpStatusCode.BadRequest, "Invalid session ID or word ID")
                return@post
            }

            val params = call.receiveParameters()
            val correct = params["correct"]?.toBoolean()
            
            if (correct == null) {
                call.respond(HttpStatusCode.BadRequest, "Missing or invalid 'correct' parameter")
                return@post
            }

            call.respond(databaseService.reviewWord(sessionId, wordId, correct))
        }
    }
}
