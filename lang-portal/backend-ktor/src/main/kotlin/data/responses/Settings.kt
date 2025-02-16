package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class Settings(
    val language: String,
    @SerialName("study_mode") val studyMode: String,
    @SerialName("daily_goal") val dailyGoal: Int,
    @SerialName("notification_enabled") val notificationEnabled: Boolean
)
