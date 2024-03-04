import java.util.Random;

/**
 * Pseudorandom Bit generator
 */
public class RandomBitGenerator {

    private static final int MAXSIZE = 128;

    /**
     * Generates and displays a set of pseudorandom bits of a given length
     *
     */
    public void generateRandomBits() {
        Random random = new Random();
        for (int i = 0; i < MAXSIZE; i++)
            System.out.print(random.nextInt(2));
    }

    public static void main(String[] args) {
        RandomBitGenerator generator = new RandomBitGenerator();
        generator.generateRandomBits();
    }
}