plugins {
    java
    `java-library`
}

group = "com.bimportal"
version = "1.0.0"

java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}

repositories {
    mavenCentral()
}

dependencies {
    // Core Feign dependencies
    api("io.github.openfeign:feign-core:13.1")
    api("io.github.openfeign:feign-jackson:13.1")
    api("io.github.openfeign:feign-slf4j:13.1")
    api("io.github.openfeign:feign-okhttp:13.1")

    // Form encoding support (required by generated client)
    api("io.github.openfeign.form:feign-form:3.8.0")

    // Jackson dependencies with JSR310 support
    api("com.fasterxml.jackson.core:jackson-databind:2.15.2")
    api("com.fasterxml.jackson.core:jackson-annotations:2.15.2")
    api("com.fasterxml.jackson.core:jackson-core:2.15.2")
    api("com.fasterxml.jackson.datatype:jackson-datatype-jsr310:2.15.2")

    // Jackson nullable support (required by generated client)
    api("org.openapitools:jackson-databind-nullable:0.2.6")

    // HTTP client
    api("com.squareup.okhttp3:okhttp:4.11.0")
    api("com.squareup.okhttp3:logging-interceptor:4.11.0")

    // OpenAPI/Swagger annotations
    api("io.swagger:swagger-annotations:1.6.8")

    // Jakarta Validation (for Spring Boot 3.x compatibility)
    api("jakarta.validation:jakarta.validation-api:3.0.2")
    api("jakarta.annotation:jakarta.annotation-api:2.1.1")
    api("org.hibernate.validator:hibernate-validator:8.0.1.Final")

    // Logging
    api("org.slf4j:slf4j-api:2.0.9")

    // Testing
    testImplementation(platform("org.junit:junit-bom:5.10.0"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")

    // Keep existing test dependencies
    testImplementation("org.mockito:mockito-core:5.5.0")
    testImplementation("io.github.cdimascio:java-dotenv:5.2.2")
}

tasks.test {
    useJUnitPlatform()
}

// Fix incorrect imports and configure Jackson properly in generated code
// Fix incorrect imports and configure Jackson properly in generated code
tasks.register("fixGeneratedCode") {
    description = "Fix incorrect imports and configure Jackson in generated OpenAPI client code"
    doLast {
        val srcDir = file("src/main/java")
        if (srcDir.exists()) {
            srcDir.walkTopDown()
                .filter { it.name.endsWith(".java") }
                .forEach { file ->
                    val content = file.readText()
                    var modified = content

                    // Fix RequestLine import
                    modified = modified.replace(
                        "import org.gradle.internal.impldep.org.apache.http.RequestLine;",
                        "import feign.RequestLine;"
                    )

                    // Fix Headers import
                    modified = modified.replace(
                        "import org.junit.jupiter.params.shadow.com.univocity.parsers.annotations.Headers;",
                        "import feign.Headers;"
                    )

                    // Fix deprecated QueryMap encoded parameter
                    modified = modified.replace(
                        "@QueryMap(encoded=true)",
                        "@QueryMap"
                    )

//                    // Fix ApiClient.java to properly configure Jackson with JSR310 support
//                    if (file.name == "ApiClient.java") {
//                        // Add class-level suppression if not already present
//                        if (!modified.contains("@SuppressWarnings") && modified.contains("public class ApiClient")) {
//                            modified = modified.replace(
//                                "public class ApiClient",
//                                "@SuppressWarnings({\"unchecked\", \"rawtypes\"})\npublic class ApiClient"
//                            )
//                        }
//
//                        // Replace the entire createObjectMapper method with a properly configured one
//                        val createObjectMapperRegex = Regex(
//                            """private ObjectMapper createObjectMapper\(\) \{[^}]+\}""",
//                            RegexOption.DOT_MATCHES_ALL
//                        )
//
//                        val newCreateObjectMapper = """private ObjectMapper createObjectMapper() {
//    ObjectMapper objectMapper = new ObjectMapper();
//
//    // Register JSR310 module first for proper date/time handling
//    objectMapper.registerModule(new JavaTimeModule());
//
//    // Then register other modules
//    objectMapper.findAndRegisterModules();
//
//    // Configure serialization features
//    objectMapper.enable(SerializationFeature.WRITE_ENUMS_USING_TO_STRING);
//    objectMapper.enable(DeserializationFeature.READ_ENUMS_USING_TO_STRING);
//    objectMapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
//    objectMapper.disable(DeserializationFeature.FAIL_ON_INVALID_SUBTYPE);
//    objectMapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
//
//    // Critical fix for nanosecond precision timestamps in BIM Portal responses
//    objectMapper.configure(DeserializationFeature.READ_DATE_TIMESTAMPS_AS_NANOSECONDS, false);
//
//    // Set date format
//    objectMapper.setDateFormat(new RFC3339DateFormat());
//
//    // Add JsonNullable module
//    JsonNullableModule jnm = new JsonNullableModule();
//    objectMapper.registerModule(jnm);
//
//    return objectMapper;
//  }"""
//
//                        modified = createObjectMapperRegex.replace(modified, newCreateObjectMapper)
//                    }

                    // Add method-level suppression for API classes with QueryMap deprecation warnings
                    if (file.name.endsWith("Api.java") && modified.contains("@QueryMap")) {
                        val lines = modified.lines().toMutableList()
                        var i = 0
                        while (i < lines.size) {
                            val line = lines[i]
                            if (line.contains("@QueryMap") && i > 0) {
                                val prevLine = lines[i - 1].trim()
                                if (!prevLine.contains("@SuppressWarnings")) {
                                    val indent = lines[i].takeWhile { it.isWhitespace() }
                                    lines.add(i, "${indent}@SuppressWarnings(\"deprecation\")")
                                    i++
                                }
                            }
                            i++
                        }
                        modified = lines.joinToString("\n")
                    }

                    if (modified != content) {
                        file.writeText(modified)
                        println("Fixed code issues in: ${file.relativeTo(srcDir)}")
                    }
                }
        }
    }
}
// Configure compiler options
tasks.compileJava {
    dependsOn("fixGeneratedCode")
    options.encoding = "UTF-8"

    // Remove -Werror and configure appropriate warnings
    options.compilerArgs.addAll(listOf(
        "-Xlint:unchecked",
        "-Xlint:deprecation",
        "-Xlint:-processing"  // Suppress annotation processing warnings
        // Note: Removed -Werror to prevent warnings from failing the build
    ))

    // Set source and target compatibility explicitly
    sourceCompatibility = JavaVersion.VERSION_21.toString()
    targetCompatibility = JavaVersion.VERSION_21.toString()
}