rmse <- read.csv("../data/RMSE.csv")
rmse
barplot(as.matrix(rmse[,2:5]))

library(ggplot2)
install.packages("ggplot2")

ggplot(rmse[,2:5], legend.text = rmse$ADCP, beside=T, 
        main = "Root mean squared error ADCP vs ADV different sections",
        col= c('mediumblue', 'mediumslateblue', "Red"), xlab = "Postion", 
        ylab = "RMSE (m^3/s)", ylim = c(0,0.8))

text(y = as.matrix(rmse[,2:5]))

help(barplot)

as.matrix(rmse[,2:5])

asm <- as.matrix(rmse[,2:5])

casm = c(asm)
asm2 <- round(asm, digits = 3)
asm3 <- asm2

plt <- barplot(as.matrix(rmse[,2:5]), beside=T, 
        main = "Root mean squared error ADCP vs ADV different sections",
        col= c('mediumblue', 'mediumslateblue', "Red"), xlab = "Postion", 
        ylab = "RMSE (m^3/s)", ylim = c(0,0.70), border = "white", args.legend = "topleft")

legend("topleft", legend = rmse$ADCP, inset = 0.05)
y<-as.matrix(rmse)

asm3[2]=asm3[2]+0.01
asm3[11]=asm3[11]+0.01

text(x = plt, y = c(asm3)+0.02, labels = c(asm2), cex = 0.7)

help(legend)

help(text)

help(text)

asm[,2]

asm[2,]

plt <- barplot(as.matrix(rmse[,2:5]), legend.text = rmse$ADCP, beside=T, 
               main = "Root mean squared error ADCP vs ADV different sections",
               col= c('mediumblue', 'mediumslateblue', "Red"), xlab = "Postion", 
               ylab = "RMSE (m^3/s)", ylim = c(0,0.87), border = "white", args.legend = "topleft")
