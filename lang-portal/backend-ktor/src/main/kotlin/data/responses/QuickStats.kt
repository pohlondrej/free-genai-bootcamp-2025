package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.Serializable

@Serializable
data class QuickStats(
    val successRate: Double,
    val totalStudySessions: Int,
    val totalActiveGroups: Int,
    val studyStreakDays: Int
)
