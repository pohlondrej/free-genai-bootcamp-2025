package com.pohlondrej.langportal.backend.data

import org.jetbrains.exposed.sql.Table
import org.jetbrains.exposed.sql.Column
import org.jetbrains.exposed.sql.javatime.datetime
import java.time.LocalDateTime

object Words : Table("words") {
    val id: Column<Int> = integer("id").autoIncrement()
    val japanese: Column<String> = varchar("japanese", 255)
    val romaji: Column<String> = varchar("romaji", 255)
    val english: Column<String> = varchar("english", 255)

    override val primaryKey: PrimaryKey = PrimaryKey(id)
}

object WordGroups : Table("word_groups") {
    val id: Column<Int> = integer("id").autoIncrement()
    val wordId: Column<Int> = integer("word_id").references(Words.id)
    val groupId: Column<Int> = integer("group_id").references(Groups.id)

    override val primaryKey: PrimaryKey = PrimaryKey(id)
}

object Groups : Table("groups") {
    val id: Column<Int> = integer("id").autoIncrement()
    val name: Column<String> = varchar("name", 255)

    override val primaryKey: PrimaryKey = PrimaryKey(id)
}

object StudySessions : Table("study_sessions") {
    val id: Column<Int> = integer("id").autoIncrement()
    val groupId: Column<Int> = integer("group_id").references(Groups.id)
    val createdAt: Column<LocalDateTime> = datetime("created_at")
    val studyActivityId: Column<Int> = integer("study_activity_id").references(StudyActivities.id)

    override val primaryKey: PrimaryKey = PrimaryKey(id)
}

object StudyActivities : Table("study_activities") {
    val id: Column<Int> = integer("id").autoIncrement()
    val studySessionId: Column<Int> = integer("study_session_id").references(StudySessions.id)
    val groupId: Column<Int> = integer("group_id").references(Groups.id)
    val createdAt: Column<LocalDateTime> = datetime("created_at")

    override val primaryKey: PrimaryKey = PrimaryKey(id)
}

object WordReviewItems : Table("word_review_items") {
    val wordId: Column<Int> = integer("word_id").references(Words.id)
    val studySessionId: Column<Int> = integer("study_session_id").references(StudySessions.id)
    val correct: Column<Boolean> = bool("correct")
    val createdAt: Column<LocalDateTime> = datetime("created_at")

    override val primaryKey = PrimaryKey(arrayOf(wordId, studySessionId))
}