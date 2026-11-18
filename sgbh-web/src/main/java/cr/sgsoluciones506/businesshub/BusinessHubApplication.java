package cr.sgsoluciones506.businesshub;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * Punto de entrada de SG Business Hub.
 * Monolito modular: un paquete por módulo, cada uno con controller, service, repository, model y dto.
 */
@SpringBootApplication
@EnableScheduling
public class BusinessHubApplication {

    public static void main(String[] args) {
        SpringApplication.run(BusinessHubApplication.class, args);
    }
}
