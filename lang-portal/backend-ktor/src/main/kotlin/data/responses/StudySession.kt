package com.pohlondrej.langportal.backend.data.responses

import com.pohlondrej.langportal.backend.data.serializers.LocalDateTimeSerializer
import kotlinx.serialization.Serializable
import java.time.LocalDateTime
import kotlinx.serialization.SerialName

@Serializable
data class StudySession(
    val id: Int,
    @SerialName("group_id") val groupId: Int,
    @SerialName("activity_name") val activityName: String,
    @Serializable(with = LocalDateTimeSerializer::class)
    @SerialName("created_at") val createdAt: LocalDateTime,
    @SerialName("correct_count") val correctCount: Int,
    @SerialName("wrong_count") val wrongCount: Int,
)
