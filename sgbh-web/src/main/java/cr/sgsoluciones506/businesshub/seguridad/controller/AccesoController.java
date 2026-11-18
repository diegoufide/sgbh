package cr.sgsoluciones506.businesshub.seguridad.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

/**
 * Pantallas de inicio de sesión y página principal.
 */
@Controller
public class AccesoController {

    @GetMapping("/login")
    public String login() {
        return "seguridad/login";
    }

    @GetMapping("/")
    public String inicio() {
        return "inicio";
    }
}
