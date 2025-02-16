package com.pohlondrej.langportal.backend.data.responses

import com.pohlondrej.langportal.backend.data.serializers.LocalDateTimeSerializer
import java.time.LocalDateTime
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class WordReviewResponse(
    val success: Boolean,
    @SerialName("word_id") val wordId: Int,
    @SerialName("study_session_id") val studySessionId: Int,
    val correct: Boolean,
    @Serializable(with = LocalDateTimeSerializer::class)
    @SerialName("created_at") val createdAt: LocalDateTime
)
