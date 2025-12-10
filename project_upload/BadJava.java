// BadJava.java
// Java file missing comments, contains bad practices

public class BadJava {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
        int x = 5;
        if (x == 5)
            System.out.println("Five!");
        Runtime.getRuntime().exec("calc.exe"); // SECURITY: avoid exec
    }
}
