package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class QuickStats(
    @SerialName("total_vocabulary") val wordsTotal: Int,
    @SerialName("total_words_studied") val wordsStudiedTotal: Int,
    @SerialName("mastered_words") val wordsMastered: Int,
    @SerialName("success_rate") val successRate: Double,
    @SerialName("total_sessions") val totalStudySessions: Int,
    @SerialName("active_groups") val totalActiveGroups: Int,
    @SerialName("current_streak") val studyStreakDays: Int
)
