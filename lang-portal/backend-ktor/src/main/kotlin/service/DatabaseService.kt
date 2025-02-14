package com.pohlondrej.langportal.backend.service

import com.pohlondrej.langportal.backend.data.*
import com.pohlondrej.langportal.backend.database.*
import kotlinx.datetime.Clock
import kotlinx.datetime.Instant
import kotlinx.serialization.json.Json
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.transaction
import kotlin.math.ceil

class DatabaseService {
    fun getWords(page: Int = 1, itemsPerPage: Int = 100): Pair<List<WordWithStats>, PaginationInfo> = transaction {
        val totalItems = Words.selectAll().count()
        val totalPages = ceil(totalItems.toDouble() / itemsPerPage).toInt()
        val offset = (page - 1) * itemsPerPage

        val words = Words
            .leftJoin(WordReviewItems)
            .slice(Words.columns + listOf(
                WordReviewItems.wordId,
                WordReviewItems.correct.count(),
                Count(WordReviewItems.correct).alias("correct_count")
            ))
            .selectAll()
            .groupBy(Words.id)
            .orderBy(Words.id)
            .limit(itemsPerPage, offset.toLong())
            .map { row ->
                WordWithStats(
                    japanese = row[Words.japanese],
                    romaji = row[Words.romaji],
                    english = row[Words.english],
                    correctCount = row[Count(WordReviewItems.correct)].toInt(),
                    wrongCount = row[WordReviewItems.correct.count()].toInt() - row[Count(WordReviewItems.correct)].toInt()
                )
            }

        Pair(words, PaginationInfo(
            currentPage = page,
            totalPages = totalPages,
            totalItems = totalItems.toInt(),
            itemsPerPage = itemsPerPage
        ))
    }

    fun getWord(id: Int): WordDetails? = transaction {
        val word = Words.select { Words.id eq id }.singleOrNull() ?: return@transaction null

        val stats = WordReviewItems
            .slice(
                WordReviewItems.correct.count(),
                Count(WordReviewItems.correct).alias("correct_count")
            )
            .select { WordReviewItems.wordId eq id }
            .groupBy(WordReviewItems.wordId)
            .singleOrNull()

        val groups = (Words innerJoin WordGroups innerJoin Groups)
            .slice(Groups.columns)
            .select { Words.id eq id }
            .map { GroupBasic(it[Groups.id], it[Groups.name]) }

        WordDetails(
            id = word[Words.id],
            japanese = word[Words.japanese],
            romaji = word[Words.romaji],
            english = word[Words.english],
            stats = WordStats(
                correctCount = stats?.get(Count(WordReviewItems.correct))?.toInt() ?: 0,
                wrongCount = (stats?.get(WordReviewItems.correct.count())?.toInt() ?: 0) - (stats?.get(Count(WordReviewItems.correct))?.toInt() ?: 0)
            ),
            groups = groups
        )
    }

    fun getGroups(page: Int = 1, itemsPerPage: Int = 100): Pair<List<GroupWithCount>, PaginationInfo> = transaction {
        val totalItems = Groups.selectAll().count()
        val totalPages = ceil(totalItems.toDouble() / itemsPerPage).toInt()
        val offset = (page - 1) * itemsPerPage

        val groups = Groups
            .leftJoin(WordGroups)
            .slice(Groups.columns + WordGroups.groupId.count())
            .selectAll()
            .groupBy(Groups.id)
            .orderBy(Groups.id)
            .limit(itemsPerPage, offset.toLong())
            .map { row ->
                GroupWithCount(
                    id = row[Groups.id],
                    name = row[Groups.name],
                    wordCount = row[WordGroups.groupId.count()].toInt()
                )
            }

        Pair(groups, PaginationInfo(
            currentPage = page,
            totalPages = totalPages,
            totalItems = totalItems.toInt(),
            itemsPerPage = itemsPerPage
        ))
    }

    fun getGroup(id: Int): GroupDetails? = transaction {
        val group = Groups.select { Groups.id eq id }.singleOrNull() ?: return@transaction null

        val wordCount = WordGroups
            .slice(WordGroups.id.count())
            .select { WordGroups.groupId eq id }
            .single()[WordGroups.id.count()]

        GroupDetails(
            id = group[Groups.id],
            name = group[Groups.name],
            stats = GroupStats(
                totalWordCount = wordCount.toInt()
            )
        )
    }

    fun getGroupWords(groupId: Int, page: Int = 1, itemsPerPage: Int = 100): Pair<List<WordWithStats>, PaginationInfo> = transaction {
        val totalItems = WordGroups.select { WordGroups.groupId eq groupId }.count()
        val totalPages = ceil(totalItems.toDouble() / itemsPerPage).toInt()
        val offset = (page - 1) * itemsPerPage

        val words = (Words innerJoin WordGroups)
            .leftJoin(WordReviewItems)
            .slice(Words.columns + listOf(
                WordReviewItems.wordId,
                WordReviewItems.correct.count(),
                Count(WordReviewItems.correct).alias("correct_count")
            ))
            .select { WordGroups.groupId eq groupId }
            .groupBy(Words.id)
            .orderBy(Words.id)
            .limit(itemsPerPage, offset.toLong())
            .map { row ->
                WordWithStats(
                    japanese = row[Words.japanese],
                    romaji = row[Words.romaji],
                    english = row[Words.english],
                    correctCount = row[Count(WordReviewItems.correct)].toInt(),
                    wrongCount = row[WordReviewItems.correct.count()].toInt() - row[Count(WordReviewItems.correct)].toInt()
                )
            }

        Pair(words, PaginationInfo(
            currentPage = page,
            totalPages = totalPages,
            totalItems = totalItems.toInt(),
            itemsPerPage = itemsPerPage
        ))
    }

    fun getLastStudySession(): StudySession? = transaction {
        StudySessions
            .select { StudySessions.id greater 0 }
            .orderBy(StudySessions.createdAt to SortOrder.DESC)
            .limit(1)
            .map { row ->
                StudySession(
                    id = row[StudySessions.id],
                    groupId = row[StudySessions.groupId],
                    createdAt = row[StudySessions.createdAt],
                    studyActivityId = row[StudySessions.studyActivityId]
                )
            }
            .singleOrNull()
    }

    fun getStudyProgress(): StudyProgress = transaction {
        val totalWords = Words.selectAll().count()
        val studiedWords = WordReviewItems
            .slice(WordReviewItems.wordId)
            .selectAll()
            .withDistinct()
            .count()

        StudyProgress(
            totalWordsStudied = studiedWords.toInt(),
            totalAvailableWords = totalWords.toInt()
        )
    }

    fun getQuickStats(): QuickStats = transaction {
        val totalReviews = WordReviewItems.selectAll().count()
        val correctReviews = WordReviewItems.select { WordReviewItems.correct eq true }.count()
        val successRate = if (totalReviews > 0) (correctReviews.toDouble() / totalReviews.toDouble() * 100) else 0.0

        val totalStudySessions = StudySessions.selectAll().count()
        val activeGroups = Groups
            .slice(Groups.id)
            .selectAll()
            .withDistinct()
            .count()

        // Calculate study streak (simplified - just count consecutive days with study sessions)
        val lastStudyDates = StudySessions
            .slice(StudySessions.createdAt)
            .selectAll()
            .orderBy(StudySessions.createdAt to SortOrder.DESC)
            .map { it[StudySessions.createdAt].toString().substring(0, 10) } // Get date part only
            .distinct()

        var streakDays = 0
        if (lastStudyDates.isNotEmpty()) {
            streakDays = 1
            // TODO: Implement proper streak calculation
        }

        QuickStats(
            successRate = successRate,
            totalStudySessions = totalStudySessions.toInt(),
            totalActiveGroups = activeGroups.toInt(),
            studyStreakDays = streakDays
        )
    }

    fun getStudyActivities(): List<StudyActivity> = transaction {
        StudyActivities
            .selectAll()
            .orderBy(StudyActivities.createdAt to SortOrder.DESC)
            .map { row ->
                StudyActivity(
                    id = row[StudyActivities.id],
                    studySessionId = row[StudyActivities.studySessionId],
                    groupId = row[StudyActivities.groupId],
                    createdAt = row[StudyActivities.createdAt]
                )
            }
    }

    fun getStudyActivity(id: Int): StudyActivity? = transaction {
        StudyActivities
            .select { StudyActivities.id eq id }
            .map { row ->
                StudyActivity(
                    id = row[StudyActivities.id],
                    studySessionId = row[StudyActivities.studySessionId],
                    groupId = row[StudyActivities.groupId],
                    createdAt = row[StudyActivities.createdAt]
                )
            }
            .singleOrNull()
    }

    fun getGroupStudySessions(groupId: Int, page: Int = 1, itemsPerPage: Int = 100): Pair<List<StudySessionInfo>, PaginationInfo> = transaction {
        val totalItems = StudySessions.select { StudySessions.groupId eq groupId }.count()
        val totalPages = ceil(totalItems.toDouble() / itemsPerPage).toInt()
        val offset = (page - 1) * itemsPerPage

        val sessions = (StudySessions innerJoin Groups)
            .slice(StudySessions.columns + Groups.name)
            .select { StudySessions.groupId eq groupId }
            .orderBy(StudySessions.createdAt to SortOrder.DESC)
            .limit(itemsPerPage, offset.toLong())
            .map { row ->
                val reviewItemsCount = WordReviewItems
                    .select { WordReviewItems.studySessionId eq row[StudySessions.id] }
                    .count()

                StudySessionInfo(
                    id = row[StudySessions.id],
                    activityName = "Vocabulary Quiz", // This could be dynamic based on activity type
                    groupName = row[Groups.name],
                    startTime = row[StudySessions.createdAt],
                    endTime = row[StudySessions.createdAt], // This should be updated when we track session end time
                    reviewItemsCount = reviewItemsCount.toInt()
                )
            }

        Pair(sessions, PaginationInfo(
            currentPage = page,
            totalPages = totalPages,
            totalItems = totalItems.toInt(),
            itemsPerPage = itemsPerPage
        ))
    }

    fun getStudySessions(page: Int = 1, itemsPerPage: Int = 100): Pair<List<StudySessionInfo>, PaginationInfo> = transaction {
        val totalItems = StudySessions.selectAll().count()
        val totalPages = ceil(totalItems.toDouble() / itemsPerPage).toInt()
        val offset = (page - 1) * itemsPerPage

        val sessions = (StudySessions innerJoin Groups)
            .slice(StudySessions.columns + Groups.name)
            .selectAll()
            .orderBy(StudySessions.createdAt to SortOrder.DESC)
            .limit(itemsPerPage, offset.toLong())
            .map { row ->
                val reviewItemsCount = WordReviewItems
                    .select { WordReviewItems.studySessionId eq row[StudySessions.id] }
                    .count()

                StudySessionInfo(
                    id = row[StudySessions.id],
                    activityName = "Vocabulary Quiz", // This could be dynamic based on activity type
                    groupName = row[Groups.name],
                    startTime = row[StudySessions.createdAt],
                    endTime = row[StudySessions.createdAt], // This should be updated when we track session end time
                    reviewItemsCount = reviewItemsCount.toInt()
                )
            }

        Pair(sessions, PaginationInfo(
            currentPage = page,
            totalPages = totalPages,
            totalItems = totalItems.toInt(),
            itemsPerPage = itemsPerPage
        ))
    }

    fun getStudySession(id: Int): StudySessionInfo? = transaction {
        (StudySessions innerJoin Groups)
            .slice(StudySessions.columns + Groups.name)
            .select { StudySessions.id eq id }
            .map { row ->
                val reviewItemsCount = WordReviewItems
                    .select { WordReviewItems.studySessionId eq row[StudySessions.id] }
                    .count()

                StudySessionInfo(
                    id = row[StudySessions.id],
                    activityName = "Vocabulary Quiz", // This could be dynamic based on activity type
                    groupName = row[Groups.name],
                    startTime = row[StudySessions.createdAt],
                    endTime = row[StudySessions.createdAt], // This should be updated when we track session end time
                    reviewItemsCount = reviewItemsCount.toInt()
                )
            }
            .singleOrNull()
    }

    fun getStudySessionWords(sessionId: Int, page: Int = 1, itemsPerPage: Int = 100): Pair<List<WordWithStats>, PaginationInfo> = transaction {
        val totalItems = WordReviewItems
            .select { WordReviewItems.studySessionId eq sessionId }
            .count()
        val totalPages = ceil(totalItems.toDouble() / itemsPerPage).toInt()
        val offset = (page - 1) * itemsPerPage

        val words = (Words innerJoin WordReviewItems)
            .slice(Words.columns + listOf(
                WordReviewItems.wordId,
                WordReviewItems.correct.count(),
                Count(WordReviewItems.correct).alias("correct_count")
            ))
            .select { WordReviewItems.studySessionId eq sessionId }
            .groupBy(Words.id)
            .orderBy(Words.id)
            .limit(itemsPerPage, offset.toLong())
            .map { row ->
                WordWithStats(
                    japanese = row[Words.japanese],
                    romaji = row[Words.romaji],
                    english = row[Words.english],
                    correctCount = row[Count(WordReviewItems.correct)].toInt(),
                    wrongCount = row[WordReviewItems.correct.count()].toInt() - row[Count(WordReviewItems.correct)].toInt()
                )
            }

        Pair(words, PaginationInfo(
            currentPage = page,
            totalPages = totalPages,
            totalItems = totalItems.toInt(),
            itemsPerPage = itemsPerPage
        ))
    }

    fun getSettings(): Settings = Settings(
        language = "Japanese",
        studyMode = "Flashcards",
        dailyGoal = 50,
        notificationEnabled = true
    )

    fun createStudyActivity(groupId: Int, studyActivityId: Int): StudyActivityCreated = transaction {
        val id = StudyActivities.insert {
            it[StudyActivities.groupId] = groupId
            it[StudyActivities.studySessionId] = studyActivityId
            it[createdAt] = Clock.System.now()
        } get StudyActivities.id

        StudyActivityCreated(id, groupId)
    }

    fun resetHistory(): SuccessResponse = transaction {
        WordReviewItems.deleteAll()
        StudyActivities.deleteAll()
        StudySessions.deleteAll()

        SuccessResponse(true, "Study history has been reset")
    }

    fun fullReset(): SuccessResponse = transaction {
        WordReviewItems.deleteAll()
        StudyActivities.deleteAll()
        StudySessions.deleteAll()
        WordGroups.deleteAll()
        Words.deleteAll()
        Groups.deleteAll()

        SuccessResponse(true, "System has been fully reset")
    }

    fun reviewWord(studySessionId: Int, wordId: Int, correct: Boolean): WordReviewResponse = transaction {
        val now = Clock.System.now()
        
        WordReviewItems.insert {
            it[WordReviewItems.wordId] = wordId
            it[WordReviewItems.studySessionId] = studySessionId
            it[WordReviewItems.correct] = correct
            it[createdAt] = now
        }

        WordReviewResponse(
            success = true,
            wordId = wordId,
            studySessionId = studySessionId,
            correct = correct,
            createdAt = now
        )
    }
}
