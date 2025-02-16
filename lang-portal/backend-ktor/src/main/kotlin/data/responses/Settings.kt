package com.pohlondrej.langportal.backend.data.responses

import kotlinx.serialization.Serializable

@Serializable
data class Settings(
    val language: String,
    val studyMode: String,
    val dailyGoal: Int,
    val notificationEnabled: Boolean
)
