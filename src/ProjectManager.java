public interface ProjectManager{
  public void save_project(String filename, String pth, boolean[] chs, int viewpos, int zoom, int selFrom, int selTo, int sigHeight);
  public void load_project(String filename);
  public String getPath();
  public boolean[] getChannels();
  public int getViewpos();
  public int getZoom();
  public int[] getSelection();
  public int getSigHeight();
}
