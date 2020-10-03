public interface EEGData{
  public float[][] getSignal();
  public String[] getLabels();
  public String getPath();
  public void reloadData(String newfile);
}
