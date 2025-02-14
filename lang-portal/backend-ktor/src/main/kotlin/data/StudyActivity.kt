package com.pohlondrej.langportal.backend.data

import kotlinx.serialization.Serializable
import kotlinx.datetime.LocalDateTime
import kotlinx.serialization.SerialName

@Serializable
data class StudyActivity(
    val id: Int,
    @SerialName("study_session_id") val studySessionId: Int,
    @SerialName("group_id") val groupId: Int,
    @SerialName("created_at") val createdAt: LocalDateTime,
)
