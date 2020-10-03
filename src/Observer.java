import java.util.*;
import javax.swing.*;
import java.awt.event.*;
import java.awt.*;

public interface Observer{
  public void notif(String msg);
  public void setBounds(int x,int y);
  public void setActiveChannels(boolean[] activeChannels);
  public int getValue();
}
