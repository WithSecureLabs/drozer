import java.io.BufferedReader;
import java.io.File;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.IOException;

public class ShellWrapper {
	
  public static class CommandReader extends Thread {
	private InputStream stream;
	private String output;
	    
	public CommandReader(InputStream stream) {
	  this.stream = stream;
	  this.output = "";
	}
	    
	public void run() {
	  try {
		BufferedReader reader = new BufferedReader(new InputStreamReader(this.stream));
		String line = null;
	        	
		while (null != (line = reader.readLine())) {
		  this.output += line + "\n";
		}
	  } catch (IOException e) {
		e.printStackTrace();
	  }
	}
	    
	public String getOutput() {
	  return this.output;
	}
	    
	public void close() {
	  try {
		this.stream.close();
	  } catch (IOException e) {
		e.printStackTrace();
	  }
	}
  }
	
  public static String execute(String command) throws InterruptedException, IOException {
	File working_dir = new File("/");
	String[] environment = null;

	// executes the command using `sh -c` command (so that piping features are present)
	Process proc = Runtime.getRuntime().exec(new String[] { "sh", "-c", command }, environment, working_dir);
	
	// read the output and error streams
	CommandReader stdout = new CommandReader(proc.getInputStream());
	CommandReader stderr = new CommandReader(proc.getErrorStream());
		
	// Run streams
	stdout.start();
	stderr.start();
		
	// ... and wait for the process to finish
	proc.waitFor();
	
	stdout.join();
	stderr.join();
		
	// Collect results
	String return_value = stderr.getOutput();
	return_value += stdout.getOutput();
		
	stdout.close();
	stderr.close();
	return return_value;
  }

}
