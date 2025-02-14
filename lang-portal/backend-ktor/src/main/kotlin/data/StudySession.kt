package com.pohlondrej.langportal.backend.data

import kotlinx.serialization.Serializable
import kotlinx.datetime.LocalDateTime
import kotlinx.serialization.SerialName

@Serializable
data class StudySession(
    val id: Int,
    @SerialName("group_id") val groupId: Int,
    @SerialName("created_at") val createdAt: LocalDateTime,
    @SerialName("study_activity_id") val studyActivityId: Int,
)
