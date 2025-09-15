plugins {
    java
    application
    id("org.springframework.boot") version "3.4.0"
    id("io.spring.dependency-management") version "1.1.6"
}

dependencies {
    // Dependency on the generated OpenAPI client
    implementation(project(":openapi-generated"))

    // Spring Boot starters
    implementation("org.springframework.boot:spring-boot-starter")
    implementation("org.springframework.boot:spring-boot-starter-web")

    // Utilities using version catalog
    implementation(libs.bundles.utilities)

    // Testing
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation(libs.bundles.testing)
}

application {
    mainClass.set("com.pb40.bimportal.examples.QuickStart")
}

tasks.jar {
    dependsOn(":openapi-generated:jar")
    manifest {
        attributes["Main-Class"] = "com.pb40.bimportal.examples.QuickStart"
    }
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE
    from(configurations.runtimeClasspath.get().map { if (it.isDirectory) it else zipTree(it) })
}

// Custom tasks for running examples
tasks.register<JavaExec>("quickStart") {
    group = "examples"
    description = "Run the quick start example"
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass.set("com.pb40.bimportal.examples.QuickStart")
}

//tasks.register<JavaExec>("exportExamples") {
//    group = "examples"
//    description = "Run comprehensive export examples"
//    classpath = sourceSets.main.get().runtimeClasspath
//    mainClass.set("com.pb40.bimportal.examples.ExportExamples")
//}


tasks.register<JavaExec>("healthCheck") {
    group = "examples"
    description = "Run API health check"
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass.set("com.pb40.bimportal.examples.HealthCheck")
}

tasks.register<JavaExec>("checkApiMethods") {
    group = "examples"
    description = "Check available methods in generated API classes"
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass.set("com.pb40.bimportal.client.ApiMethodChecker")
}


// New independent export examples
tasks.register<JavaExec>("exportProjects") {
    group = "examples"
    description = "Export projects in multiple formats (PDF, OpenOffice, OKSTRA, LOIN-XML, IDS)"
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass.set("com.pb40.bimportal.examples.ProjectExportExample")
}

tasks.register<JavaExec>("exportLoins") {
    group = "examples"
    description = "Export LOINs in multiple formats (PDF, OpenOffice, OKSTRA, LOIN-XML, IDS)"
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass.set("com.pb40.bimportal.examples.LoinExportExample")
}

tasks.register<JavaExec>("exportDomainModels") {
    group = "examples"
    description = "Export domain models in multiple formats (PDF, OpenOffice, OKSTRA, LOIN-XML, IDS)"
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass.set("com.pb40.bimportal.examples.DomainModelExportExample")
}

tasks.register<JavaExec>("exportContextInfo") {
    group = "examples"
    description = "Export context information in multiple formats (PDF, OpenOffice)"
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass.set("com.pb40.bimportal.examples.ContextInfoExportExample")
}

tasks.register<JavaExec>("exportTemplates") {
    group = "examples"
    description = "Export AIA templates in multiple formats (PDF, OpenOffice)"
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass.set("com.pb40.bimportal.examples.TemplateExportExample")
}

tasks.register<JavaExec>("batchExport") {
    group = "examples"
    description = "Run batch export examples for multiple projects and LOINs"
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass.set("com.pb40.bimportal.examples.BatchExportExample")
}

tasks.register<JavaExec>("searchExamples") {
    group = "examples"
    description = "Run search and filter examples"
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass.set("com.pb40.bimportal.examples.SearchExample")
}

tasks.register<JavaExec>("organizationExample") {
    group = "examples"
    description = "Run organizationexamples"
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass.set("com.pb40.bimportal.examples.OrganizationExample")
}

// Convenience task to run all export examples
tasks.register("runAllExportExamples") {
    group = "examples"
    description = "Run all export examples sequentially"
    dependsOn(
        "exportProjects",
        "exportLoins",
        "exportDomainModels",
        "exportContextInfo",
        "exportTemplates",
        "batchExport",
        "searchExamples",
        "organizationExample"
    )

    doLast {
        println("All export examples completed!")
    }
}

// Resource processing
tasks.processResources {
    val projectProps = project.properties
    filesMatching("application.properties") {
        expand(projectProps)
    }
}