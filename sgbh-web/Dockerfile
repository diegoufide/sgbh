FROM maven:3.9-eclipse-temurin-21 AS construccion
WORKDIR /app
COPY pom.xml .
RUN mvn -B -q dependency:go-offline
COPY src ./src
RUN mvn -B -q package -DskipTests

FROM eclipse-temurin:21-jre
WORKDIR /app
RUN useradd --system --uid 1001 sgbh
COPY --from=construccion /app/target/businesshub-*.jar /app/sgbh-web.jar
USER sgbh
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/sgbh-web.jar"]
