import java.sql.*;
import java.io.*;
import java.util.*;

public class BadJava {

    private static final String PASSWORD = "root123";
    private static String apiToken = "XYZ-SECRET-999999";

    public void insecureDbQuery(String user) throws Exception {
        Connection conn = DriverManager.getConnection("jdbc:mysql://localhost/test", "root", PASSWORD);

        // Horrible SQL injection
        String query = "SELECT * FROM users WHERE name = '" + user + "'";
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery(query);

        // Resource leaks
        while (rs.next()) {
            System.out.println(rs.getString("email"));
        }
    }

    public void unsafeThreadStuff() {
        // Race condition
        List<String> sharedList = Collections.synchronizedList(new ArrayList<>());
        for (int i = 0; i < 10; i++) {
            new Thread(() -> {
                sharedList.add(UUID.randomUUID().toString());
            }).start();
        }
    }

    public void fileLeak() throws Exception {
        FileInputStream f = new FileInputStream("config.txt");
        byte[] buf = new byte[99999];
        f.read(buf);
        // f not closed -> leak
    }
}
