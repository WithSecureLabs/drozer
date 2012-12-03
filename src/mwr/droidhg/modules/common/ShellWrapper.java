import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.io.IOException;

public class ShellWrapper {

  public static String execute(String command) throws InterruptedException, IOException {
    File working_dir = new File("/");
    String[] environment = null;

    // executes the command using `sh -c` command (so that piping features are present)
    Process proc = Runtime.getRuntime().exec(new String[] { "sh", "-c", command }, environment, working_dir);
    // ... and wait for the process to finish
    proc.waitFor();
    
    // read the output and error streams
    BufferedReader stdout = new BufferedReader(new InputStreamReader(proc.getInputStream()));
    BufferedReader stderr = new BufferedReader(new InputStreamReader(proc.getErrorStream()));
    
    String line;
    String return_value = "";

    while((line = stderr.readLine()) != null)
      return_value += line + "\n";
    while((line = stdout.readLine()) != null)
      return_value += line + "\n";

    return return_value;
  }

}
