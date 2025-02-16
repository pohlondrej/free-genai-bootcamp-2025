package com.pohlondrej.langportal.backend.data.responses

import com.pohlondrej.langportal.backend.data.serializers.LocalDateTimeSerializer
import java.time.LocalDateTime
import kotlinx.serialization.Serializable

@Serializable
data class WordReviewResponse(
    val success: Boolean,
    val wordId: Int,
    val studySessionId: Int,
    val correct: Boolean,
    @Serializable(with = LocalDateTimeSerializer::class)
    val createdAt: LocalDateTime
)
