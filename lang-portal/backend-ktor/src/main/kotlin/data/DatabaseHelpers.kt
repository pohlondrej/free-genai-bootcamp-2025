package com.pohlondrej.langportal.backend.data

import com.pohlondrej.langportal.backend.data.responses.GroupBasic
import com.pohlondrej.langportal.backend.data.responses.GroupDetails
import com.pohlondrej.langportal.backend.data.responses.GroupStats
import com.pohlondrej.langportal.backend.data.responses.GroupWithCount
import com.pohlondrej.langportal.backend.data.responses.PaginationInfo
import com.pohlondrej.langportal.backend.data.responses.QuickStats
import com.pohlondrej.langportal.backend.data.responses.Settings
import com.pohlondrej.langportal.backend.data.responses.StudyActivityCreated
import com.pohlondrej.langportal.backend.data.responses.StudyProgress
import com.pohlondrej.langportal.backend.data.responses.StudySession
import com.pohlondrej.langportal.backend.data.responses.StudySessionInfo
import com.pohlondrej.langportal.backend.data.responses.SuccessResponse
import com.pohlondrej.langportal.backend.data.responses.WordDetails
import com.pohlondrej.langportal.backend.data.responses.WordReviewResponse
import com.pohlondrej.langportal.backend.data.responses.WordWithStats
import kotlin.math.ceil
import kotlinx.datetime.Clock
import kotlinx.datetime.TimeZone
import kotlinx.datetime.toJavaLocalDateTime
import kotlinx.datetime.toLocalDateTime
import org.jetbrains.exposed.sql.Count
import org.jetbrains.exposed.sql.Op
import org.jetbrains.exposed.sql.SortOrder
import org.jetbrains.exposed.sql.SqlExpressionBuilder
import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.SqlExpressionBuilder.greater
import org.jetbrains.exposed.sql.alias
import org.jetbrains.exposed.sql.and
import org.jetbrains.exposed.sql.count
import org.jetbrains.exposed.sql.deleteAll
import org.jetbrains.exposed.sql.insert
import org.jetbrains.exposed.sql.min
import org.jetbrains.exposed.sql.select
import org.jetbrains.exposed.sql.selectAll
import org.jetbrains.exposed.sql.transactions.transaction

fun getWords(page: Int = 1, itemsPerPage: Int = 100): Pair<List<WordWithStats>, PaginationInfo> = transaction {
    val totalItems = Words.selectAll().count()
    val totalPages = ceil(totalItems.toDouble() / itemsPerPage).toInt()
    val offset = (page - 1) * itemsPerPage

    val words = Words
        .leftJoin(WordReviewItems)
        .select(
            Words.columns + listOf(
                WordReviewItems.wordId,
                WordReviewItems.correct.count(),
                Count(WordReviewItems.correct).alias("correct_count")
            )
        )
        .groupBy(Words.id)
        .orderBy(Words.id)
        .limit(itemsPerPage, offset.toLong())
        .map { row ->
            WordWithStats(
                id = row[Words.id],
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
    val word = Words.selectAll().where { Words.id eq id }.singleOrNull() ?: return@transaction null

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
        correctCount = stats?.get(Count(WordReviewItems.correct))?.toInt() ?: 0,
        wrongCount = (stats?.get(WordReviewItems.correct.count())?.toInt() ?: 0) - (stats?.get(Count(WordReviewItems.correct))?.toInt() ?: 0),
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

fun getGroup(id: Int): GroupWithCount? = transaction {
    val group = Groups.select { Groups.id eq id }.singleOrNull() ?: return@transaction null

    val wordCount = WordGroups
        .slice(WordGroups.id.count())
        .select { WordGroups.groupId eq id }
        .single()[WordGroups.id.count()]

    GroupWithCount(
        id = group[Groups.id],
        name = group[Groups.name],
        wordCount = wordCount.toInt()
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
                id = row[Words.id],
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
        .selectAll().where { StudySessions.id greater 0 }
        .orderBy(StudySessions.createdAt to SortOrder.DESC)
        .limit(1)
        .mapNotNull { row ->
            val correctCount = WordReviewItems
                .selectAll().where { WordReviewItems.studySessionId eq row[StudySessions.id] and (WordReviewItems.correct eq true) }
                .count()
            val wrongCount = WordReviewItems
                .selectAll().where { WordReviewItems.studySessionId eq row[StudySessions.id] and (WordReviewItems.correct eq false) }
                .count()

            StudySession(
                id = row[StudySessions.id],
                groupId = row[StudySessions.groupId],
                activityName = "Vocabulary Quiz", // Hardcoded activity name as per other functions
                createdAt = row[StudySessions.createdAt],
                correctCount = correctCount.toInt(),
                wrongCount = wrongCount.toInt()
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
    val totalWords = Words.selectAll().count()
    val wordsStudied = (Words innerJoin WordReviewItems)
        .select(Words.columns)
        .withDistinct()
        .map { row ->
            Word(
                id = row[Words.id],
                japanese = row[Words.japanese],
                romaji = row[Words.romaji],
                english = row[Words.english],
            )
        }
    val masteredWordsCount = (Words innerJoin WordReviewItems)
        .select(Words.id)
        .groupBy(Words.id)
        .having { WordReviewItems.correct.min() eq true } // Ensure all reviews are correct
        .withDistinct()
        .count()

    val totalWordsStudied = wordsStudied.count()

    val totalReviews = WordReviewItems.selectAll().count()
    val correctReviews = WordReviewItems.selectAll().where { WordReviewItems.correct eq true }.count()
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
        wordsTotal = totalWords.toInt(),
        wordsStudiedTotal = totalWordsStudied,
        wordsMastered = masteredWordsCount.toInt(),
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
    val totalItems = StudySessions.selectAll().where { StudySessions.groupId eq groupId }.count()
    val totalPages = ceil(totalItems.toDouble() / itemsPerPage).toInt()
    val offset = (page - 1) * itemsPerPage

    val sessions = (StudySessions innerJoin Groups)
        .select(StudySessions.columns + Groups.name)
        .where { StudySessions.groupId eq groupId }
        .orderBy(StudySessions.createdAt to SortOrder.DESC)
        .limit(itemsPerPage, offset.toLong())
        .map { row ->
            val reviewItemsCount = WordReviewItems
                .selectAll().where { WordReviewItems.studySessionId eq row[StudySessions.id] }
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
                id = row[Words.id],
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
    )
    )
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
        it[createdAt] = Clock.System.now().toLocalDateTime(TimeZone.UTC).toJavaLocalDateTime()
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
    val now = Clock.System.now().toLocalDateTime(TimeZone.UTC).toJavaLocalDateTime()

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