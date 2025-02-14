package com.pohlondrej.langportal.backend.data

import kotlinx.datetime.Instant
import kotlinx.serialization.Serializable

@Serializable
data class PaginationInfo(
    val currentPage: Int,
    val totalPages: Int,
    val totalItems: Int,
    val itemsPerPage: Int
)

@Serializable
data class WordWithStats(
    val japanese: String,
    val romaji: String,
    val english: String,
    val correctCount: Int,
    val wrongCount: Int
)

@Serializable
data class WordStats(
    val correctCount: Int,
    val wrongCount: Int
)

@Serializable
data class GroupBasic(
    val id: Int,
    val name: String
)

@Serializable
data class WordDetails(
    val id: Int,
    val japanese: String,
    val romaji: String,
    val english: String,
    val stats: WordStats,
    val groups: List<GroupBasic>
)

@Serializable
data class GroupWithCount(
    val id: Int,
    val name: String,
    val wordCount: Int
)

@Serializable
data class GroupStats(
    val totalWordCount: Int
)

@Serializable
data class GroupDetails(
    val id: Int,
    val name: String,
    val stats: GroupStats
)

@Serializable
data class StudySessionInfo(
    val id: Int,
    val activityName: String,
    val groupName: String,
    val startTime: Instant,
    val endTime: Instant,
    val reviewItemsCount: Int
)

@Serializable
data class StudyProgress(
    val totalWordsStudied: Int,
    val totalAvailableWords: Int
)

@Serializable
data class QuickStats(
    val successRate: Double,
    val totalStudySessions: Int,
    val totalActiveGroups: Int,
    val studyStreakDays: Int
)

@Serializable
data class PaginatedResponse<T>(
    val items: List<T>,
    val pagination: PaginationInfo
)

@Serializable
data class Settings(
    val language: String,
    val studyMode: String,
    val dailyGoal: Int,
    val notificationEnabled: Boolean
)

@Serializable
data class StudyActivityCreated(
    val id: Int,
    val groupId: Int
)

@Serializable
data class SuccessResponse(
    val success: Boolean,
    val message: String
)

@Serializable
data class WordReviewResponse(
    val success: Boolean,
    val wordId: Int,
    val studySessionId: Int,
    val correct: Boolean,
    val createdAt: Instant
)
