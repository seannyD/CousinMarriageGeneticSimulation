library(ggplot2)
setwd("~/Documents/Bristol/EXCD/MarriageSim/")
d = read.csv("res.csv")

d$Husband_is_father = as.factor(1-d$parental_uncertainty)
d$Husband_is_father = factor(d$Husband_is_father, levels=rev(levels(d$Husband_is_father)))

pdf("results.pdf", width=6, height=4)
ggplot(d[!is.na(d$marriageRule),],
       aes(x=gen, y = diversity, colour= Husband_is_father)) +
      stat_smooth(aes(colour=Husband_is_father)) + facet_wrap(~marriageRule) +
      xlab("Generation") + ylab("")

dev.off()