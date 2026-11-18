package cr.sgsoluciones506.businesshub.comun;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.math.BigDecimal;
import org.junit.jupiter.api.Test;

class MontosTest {

    @Test
    void debeCalcularIvaDelTrecePorCiento() {
        assertEquals(new BigDecimal("13.00"), Montos.calcularIva(new BigDecimal("100.00")));
    }

    @Test
    void debeCalcularTotalCuandoHayDescuento() {
        BigDecimal total = Montos.calcularTotal(new BigDecimal("150000.00"), new BigDecimal("10000.00"));
        assertEquals(new BigDecimal("158200.00"), total);
    }

    @Test
    void debeRechazarDescuentoMayorQueSubtotal() {
        assertThrows(IllegalArgumentException.class,
            () -> Montos.calcularTotal(new BigDecimal("100.00"), new BigDecimal("200.00")));
    }
}
