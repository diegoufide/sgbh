package cr.sgsoluciones506.businesshub.comun;

import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * Cálculos de montos en colones con IVA (RNF-012).
 */
public final class Montos {

    public static final BigDecimal TASA_IVA = new BigDecimal("0.13");
    public static final int DECIMALES = 2;

    private Montos() {
    }

    public static BigDecimal redondear(BigDecimal monto) {
        return monto.setScale(DECIMALES, RoundingMode.HALF_UP);
    }

    public static BigDecimal calcularIva(BigDecimal baseImponible) {
        return redondear(baseImponible.multiply(TASA_IVA));
    }

    public static BigDecimal calcularTotal(BigDecimal subtotal, BigDecimal descuento) {
        BigDecimal base = subtotal.subtract(descuento);
        if (base.signum() < 0) {
            throw new IllegalArgumentException("El descuento no puede ser mayor que el subtotal");
        }
        return redondear(base.add(calcularIva(base)));
    }
}
