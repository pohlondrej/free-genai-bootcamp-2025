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
    val id = integer("id").autoIncrement()
    val wordId = reference("word_id", Words.id)
    val studySessionId = reference("study_session_id", StudySessions.id)
    val correct = bool("correct")
    val createdAt = timestamp("created_at")

    override val primaryKey = PrimaryKey(id)
}

object DatabaseFactory {
    private val isDevelopment = System.getenv("ENVIRONMENT")?.lowercase() == "development"
    
    fun init() {
        val dbName = if (isDevelopment) "data_dev.db" else "data.db"
        val databasePath = dbName
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
            
            if (isDevelopment) {
                initializeTestData()
            }
        }
    }
    
    private fun initializeTestData() {
        // Only add test data if tables are empty
        if (Words.selectAll().count() > 0) return
        
        // Add test groups
        val basicGroup = Groups.insert {
            it[name] = "Basic Japanese"
        } get Groups.id
        
        val numbersGroup = Groups.insert {
            it[name] = "Numbers"
        } get Groups.id
        
        // Add test words
        val word1 = Words.insert {
            it[japanese] = "こんにちは"
            it[romaji] = "konnichiwa"
            it[english] = "hello"
        } get Words.id
        
        val word2 = Words.insert {
            it[japanese] = "さようなら"
            it[romaji] = "sayounara"
            it[english] = "goodbye"
        } get Words.id
        
        val word3 = Words.insert {
            it[japanese] = "一"
            it[romaji] = "ichi"
            it[english] = "one"
        } get Words.id
        
        val word4 = Words.insert {
            it[japanese] = "二"
            it[romaji] = "ni"
            it[english] = "two"
        } get Words.id
        
        // Add words to groups
        WordGroups.insert {
            it[wordId] = word1
            it[groupId] = basicGroup
        }
        
        WordGroups.insert {
            it[wordId] = word2
            it[groupId] = basicGroup
        }
        
        WordGroups.insert {
            it[wordId] = word3
            it[groupId] = numbersGroup
        }
        
        WordGroups.insert {
            it[wordId] = word4
            it[groupId] = numbersGroup
        }
        
        // Create a study session
        val studyActivity = StudyActivities.insert {
            it[groupId] = basicGroup
            it[createdAt] = Clock.System.now()
            it[studySessionId] = 1 // This will be updated
        } get StudyActivities.id
        
        val studySession = StudySessions.insert {
            it[groupId] = basicGroup
            it[createdAt] = Clock.System.now()
            it[studyActivityId] = studyActivity
        } get StudySessions.id
        
        // Update study activity with correct session ID
        StudyActivities.update({ StudyActivities.id eq studyActivity }) {
            it[studySessionId] = studySession
        }
        
        // Add some word reviews
        WordReviewItems.insert {
            it[wordId] = word1
            it[studySessionId] = studySession
            it[correct] = true
            it[createdAt] = Clock.System.now()
        }
        
        WordReviewItems.insert {
            it[wordId] = word2
            it[studySessionId] = studySession
            it[correct] = false
            it[createdAt] = Clock.System.now()
        }
    }
}
