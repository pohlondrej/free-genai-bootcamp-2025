val kotlin_version: String = "1.9.22"
val koin_version: String = "3.3.3"
val ktor_version: String = "2.3.0"

plugins {
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.ktor)
    alias(libs.plugins.kotlin.plugin.serialization)
}

group = "com.pohlondrej.langportal.backend"
version = "0.0.1"

application {
    mainClass.set("io.ktor.server.netty.EngineMain")

    val isDevelopment: Boolean = project.ext.has("development")
    applicationDefaultJvmArgs = listOf("-Dio.ktor.development=$isDevelopment")
}

repositories {
    mavenCentral()
}

kotlin {
    jvmToolchain(23)
}

dependencies {
    implementation(libs.ktor.server.core)
    implementation(libs.ktor.server.swagger)
    implementation(libs.ktor.server.content.negotiation)
    implementation(libs.ktor.serialization.gson)
    implementation(libs.ktor.serialization.kotlinx.json)
    implementation(libs.koin.ktor)
    implementation(libs.koin.logger.slf4j)
    implementation(libs.ktor.server.netty)
    implementation(libs.logback.classic)
    implementation(libs.ktor.server.config.yaml)
    implementation(libs.kotlinx.datetime)
    
    // Database dependencies
    implementation("org.jetbrains.exposed:exposed-core:0.41.1")
    implementation("org.jetbrains.exposed:exposed-dao:0.41.1")
    implementation("org.jetbrains.exposed:exposed-jdbc:0.41.1")
    implementation("org.jetbrains.exposed:exposed-kotlin-datetime:0.41.1")
    implementation("org.xerial:sqlite-jdbc:3.44.1.0")
    
    testImplementation(libs.ktor.server.test.host)
    testImplementation(libs.kotlin.test.junit)
    testImplementation("io.ktor:ktor-server-tests-jvm:$ktor_version")
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit:$kotlin_version")
    testImplementation("io.insert-koin:koin-test:$koin_version")
}

tasks.named<JavaExec>("run") {
    dependsOn("build")
    jvmArgs = listOf("-Dio.ktor.development=true")
}

// Custom tasks for running with different configurations
tasks.register("runDebug") {
    group = "application"
    description = "Runs the application with debug configuration"
    
    doFirst {
        project.ext["development"] = true
    }
    
    finalizedBy("run")
}