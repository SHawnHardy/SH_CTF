# TSCTF 2018 Write up

## gobang

一个五子棋游戏，主要是预处理服务器端发回的数据，至于下棋的逻辑，无非是dfs之类的，网上一大堆，在此不服赘述。

```java
	public static void main(String args[]) throws InterruptedException {
	        String host = "10.112.108.77";
	        int port = 1113;
	        Ai ai = new Ai();
	        try {
	          Socket client = new Socket(host, port);
	          OutputStream out = client.getOutputStream();//获取服务端的输出流，为了向服务端输出数据  
	          InputStream in=client.getInputStream();//获取服务端的输入流，为了获取服务端输入的数据  
	    
	          PrintWriter bufw=new PrintWriter(out,true);  
	          BufferedReader bufr=new BufferedReader(new InputStreamReader(in)); 
	          
	          
	          String play[][] = {
	             {"AA","AB","AC","AD","AE","AF","AG","AH","AI","AJ","AK","AL","AM","AN","AO"},
	             {"BA","BB","BC","BD","BE","BF","BG","BH","BI","BJ","BK","BL","BM","BN","BO"},
	             {"CA","CB","CC","CD","CE","CF","CG","CH","CI","CJ","CK","CL","CM","CN","CO"},
	             {"DA","DB","DC","DD","DE","DF","DG","DH","DI","DJ","DK","DL","DM","DN","DO"},
	             {"EA","EB","EC","ED","EE","EF","EG","EH","EI","EJ","EK","EL","EM","EN","EO"},
	             {"FA","FB","FC","FD","FE","FF","FG","FH","FI","FJ","FK","FL","FM","FN","FO"},
	             {"GA","GB","GC","GD","GE","GF","GG","GH","GI","GJ","GK","GL","GM","GN","GO"},
	             {"HA","HB","HC","HD","HE","HF","HG","HH","HI","HJ","HK","HL","HM","HN","HO"},
	             {"IA","IB","IC","ID","IE","IF","IG","IH","II","IJ","IK","IL","IM","IN","IO"},
	             {"JA","JB","JC","JD","JE","JF","JG","JH","JI","JJ","JK","JL","JM","JN","JO"},
	             {"KA","KB","KC","KD","KE","KF","KG","KH","KI","KJ","KK","KL","KM","KN","KO"},
	             {"LA","LB","LC","LD","LE","LF","LG","LH","LI","LJ","LK","LL","LM","LN","LO"},
	             {"MA","MB","MC","MD","ME","MF","MG","MH","MI","MJ","MK","ML","MM","MN","MO"},
	             {"NA","NB","NC","ND","NE","NF","NG","NH","NI","NJ","NK","NL","NM","NN","NO"},
	             {"OA","OB","OC","OD","OE","OF","OG","OH","OI","OJ","OK","OL","OM","ON","OO"}
	          };
	          
	          int count = 1;
	          
	          while (true)   
	          {  
	        	  
	              String line=null;  
	              line=bufr.readLine();//读取服务端传来的数据  
	              
	              if(line == null){
	            	  break;
	              }
	              
	              if(count == 2 ){//抢先手
	            	  if(line.startsWith("robot move to")) break;
	            	  else if(line.startsWith("you move to")){
	            		  String s = line.substring(12, 14);
		            	  int x  = s.charAt(0)-'A' + 1;//行号
		            	  int y  = s.charAt(1)-'A' + 1;//列号
		            	  
		            	
		            	  //System.out.println(s +" "+x+" "+y);
		            	  ai.firtStep(x,y);

	            	  }
	              }
	              
	              
	              if(line.startsWith("O")){
	            	  System.out.println(line);
	            	  int x = ai.bestpoint.x - 1;//列号
	            	  int y = ai.bestpoint.y - 1;//行号
	            	  
	            	  bufw.println(play[y][x]);//发送数据给服务端   
	            	  System.out.println("my ai move to " + play[y][x]);
	            	  
	            	  System.out.println("  A B C D E F G H I J K L M N O");
	            	  for(int i=1;i<=15;++i){
	            		  char c = (char) (65+i-1) ;
	            		  System.out.print(c + " ");
	            		  for(int k=1;k<=15;++k){
	            			   
	            			  if(ai.chessBoard[i][k] == 0)
	            				  System.out.print(". ");
	            			  else if(ai.chessBoard[i][k] == 1)
	            				  System.out.print("O ");
	            			  else if(ai.chessBoard[i][k] == -1)
	            				  System.out.print("X ");
	            		  }
	            		  System.out.print("\n");
	            	  }
	            	  ++count;
	            	  Thread.sleep(200);
	            	  continue;
	              }else if(line.startsWith("robot move to")){
	            	  String s = line.substring(14, 16);
	            	  int x  = s.charAt(0)-'A' + 1;//行号
	            	  int y  = s.charAt(1)-'A' + 1;//列号
	            	  //System.out.println(s +" "+x+" "+y );
	            	   
                      Ai.putChess(y*45,x*45);//敌方ai下  
                      
                      if(!Ai.isFinished){  //我方ai下
                          Ai.isBlack=true;  
                          Ai.myAI();
                      }  
                      Ai.isFinished=false;   
    
	              }
	             
	              
	              ++count;
	              System.out.println(line);//打印服务端传来的数据  
	          } 
	          
	          
	          bufw.close();
	          bufr.close();
	          out.close();
	          in.close();
	          client.close();
	          
	          
	        } catch (IOException e) {
	          e.printStackTrace();
	        }
	        
	    }
```
	其中AI类的源码详见http://zhaidongyan.cn/alpha-beta-AIWuziqi/

## 正常的魔塔

一开始打算用CE修改钥匙数和体力值，但是没扫到，放弃。

根据游戏开始时的hint，觉得游戏中会有一些bug。后来发现按h键可进入游戏配置界面，
可以修改当前所在的楼层层数。利用这个bug浏览了所有楼层后，在50层遇到交易py的老头，说要
把所有怪物杀光？？？？

无奈之下搜刮所有楼层的有用资源，在30找到了加100攻100防的宝石，还在32层的商店发现了
另外bug--金钱数大于21就可以购买8000生命或8钥匙，而不需要达到商店老板声称的160.
有了30层的宝石后低楼层的怪物就是渣渣，收集金币后到32层刷生命和钥匙，接下来就是时间的问题
了。杀光所有怪物到50层找老头即可达到flag.