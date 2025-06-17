import java.util.Date;
import java.util.Vector;

public class Main {
    public static void main(String[] args) {
        Date d = new Date();
        Vector list = new Vector();
        Runnable r = new Runnable() {
            public void run() {
                System.out.println("Legacy Code!");
            }
        };
        System.gc();
    }
}
