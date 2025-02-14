package com.pohlondrej.langportal.backend.database

import kotlinx.datetime.Clock
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.kotlin.datetime.timestamp
import org.jetbrains.exposed.sql.transactions.transaction

object Words : Table() {
    val id = integer("id").autoIncrement()
    val japanese = varchar("japanese", 255)
    val romaji = varchar("romaji", 255)
    val english = varchar("english", 255)
    val parts = text("parts").nullable()

    override val primaryKey = PrimaryKey(id)
}

object Groups : Table() {
    val id = integer("id").autoIncrement()
    val name = varchar("name", 255)

    override val primaryKey = PrimaryKey(id)
}

object WordGroups : Table() {
    val id = integer("id").autoIncrement()
    val wordId = reference("word_id", Words.id)
    val groupId = reference("group_id", Groups.id)

    override val primaryKey = PrimaryKey(id)
}

object StudySessions : Table() {
    val id = integer("id").autoIncrement()
    val groupId = reference("group_id", Groups.id)
    val createdAt = timestamp("created_at")
    val studyActivityId = reference("study_activity_id", StudyActivities.id)

    override val primaryKey = PrimaryKey(id)
}

object StudyActivities : Table() {
    val id = integer("id").autoIncrement()
    val studySessionId = reference("study_session_id", StudySessions.id)
    val groupId = reference("group_id", Groups.id)
    val createdAt = timestamp("created_at")

    override val primaryKey = PrimaryKey(id)
}

object WordReviewItems : Table() {
    val wordId = reference("word_id", Words.id)
    val studySessionId = reference("study_session_id", StudySessions.id)
    val correct = bool("correct")
    val createdAt = timestamp("created_at")

    override val primaryKey = PrimaryKey(wordId, studySessionId)
}

object DatabaseFactory {
    fun init() {
        val databasePath = "data.db" // SQLite database file
        val url = "jdbc:sqlite:$databasePath"
        
        Database.connect(url, "org.sqlite.JDBC")
        
        transaction {
            // Create all tables
            SchemaUtils.create(
                Words,
                Groups,
                WordGroups,
                StudySessions,
                StudyActivities,
                WordReviewItems
            )
        }
    }
}
