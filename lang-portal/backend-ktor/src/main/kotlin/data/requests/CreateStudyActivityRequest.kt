package com.pohlondrej.langportal.backend.data.requests

import kotlinx.serialization.Serializable
import kotlinx.serialization.SerialName

@Serializable
data class CreateStudyActivityRequest(
    @SerialName("group_id") val groupId: Int,
    @SerialName("study_activity_id") val studyActivityId: Int,
)
