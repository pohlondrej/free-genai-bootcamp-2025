package com.pohlondrej.langportal.backend.data

import com.pohlondrej.langportal.backend.data.serializers.LocalDateTimeSerializer
import java.time.LocalDateTime
import kotlinx.serialization.Serializable
import kotlinx.serialization.SerialName

@Serializable
data class StudyActivity(
    val id: Int,
    @SerialName("study_session_id") val studySessionId: Int,
    @SerialName("group_id") val groupId: Int,
    @Serializable(with = LocalDateTimeSerializer::class)
    @SerialName("created_at") val createdAt: LocalDateTime,
)
