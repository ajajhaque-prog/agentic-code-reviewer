// Advanced Java: deserialization and reflection abuse
import java.io.*;
import java.util.*;
public class AdvJava {
    public static Object deserialize(byte[] data) throws Exception {
        ByteArrayInputStream bis = new ByteArrayInputStream(data);
        ObjectInputStream ois = new ObjectInputStream(bis);
        return ois.readObject(); // unsafe deserialization
    }

    public void reflectiveCall(String className) throws Exception {
        Class<?> c = Class.forName(className);
        Object o = c.getDeclaredConstructor().newInstance();
        c.getMethod("run").invoke(o); // reflection execution
    }
}
