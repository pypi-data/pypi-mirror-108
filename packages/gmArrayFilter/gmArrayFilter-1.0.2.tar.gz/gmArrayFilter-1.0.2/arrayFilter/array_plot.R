suppressMessages(library(data.table))
suppressMessages(library(ggplot2))
suppressMessages(library(RColorBrewer))
suppressMessages(library(argparser))
suppressMessages(library(stringr))
suppressMessages(library(reshape2))
suppressMessages(library(foreach))
suppressMessages(library(doParallel))

# TODO BLANK IN FIGURE FOR SOME GENOME

options(stringsAsFactors = F)

p <- arg_parser("array density plot")
p <- add_argument(
  p, '--input', 
  help = 'input table')
p <- add_argument(
  p, '--output', 
  help = 'output prefix')
p <- add_argument(
  p, '--title',
  help = 'plot title',
  default="")
argv <- parse_args(p)

stats_table <- argv$input
output_prefix <- argv$output
plot_title <- argv$title
chr.size <- argv$chr_size


replace_zero <- function(num_count) {
  if (num_count == 0) {
    return(-Inf)
  } else {
    return(num_count)
  }
}

cor_plot_col <- colorRampPalette(brewer.pal(11, 'RdYlGn'))(100)

drawOne <- function(plot_data, output_prefix) {
  
  chrom_list <- as.character(unique(plot_data$chrom))
  chrom_pos <- 2 *seq(length(chrom_list))
  plot_data$chrom_pos <- chrom_pos[plot_data$chrom]
  plot_data$variantCount2 <- sapply(plot_data$variantCount, replace_zero)
  
  mega_base = floor(log10(max(plot_data$end)))
  mega_unit = str_pad('M', mega_base - 6 + 1,  pad = "0")
  max_chr_len = ceiling(max(plot_data$end)/(10^mega_base))
  
  p <- ggplot(plot_data) + 
    geom_rect(aes(xmin=start, xmax=end, ymin=0, 
                  ymax=1, fill = variantCount2)) +
    facet_grid(chrom~.) +
    theme(strip.text.y = element_text(size=rel(.8), 
                                      face="bold",
                                      angle = 0),
          axis.text.y = element_blank(),
          axis.ticks = element_blank(),
          panel.background = element_rect(fill = "white"),
          plot.title = element_text(hjust = 0.5, size=rel(.8))
    ) +
    scale_x_continuous(limits = c(0, max_chr_len * 10^mega_base), 
                       breaks = seq(0, max_chr_len * 10^mega_base, 10^mega_base),
                       labels = c(0, paste0(seq(1, max_chr_len), mega_unit, sep = ""))) +
    guides(fill=guide_colourbar(title='Number of SNP')) +
    xlab('Chromosome Length') + ylab('') +
    ggtitle(plot_title)
  
  if (max(plot_data$variantCount) > 1){
    p <- p + scale_fill_gradientn(colours = rev(cor_plot_col), na.value = "grey80")
  } else {
    print(unique(plot_data$variantCount2))
    p <- p + scale_fill_gradient(limits=c(0,1), low=cor_plot_col[100], high=cor_plot_col[1], na.value = "grey80", breaks=NULL)
  }
  
  chrom_num <- length(chrom_list)
  p_height = 2 * chrom_num / 7
  ggsave(paste(output_prefix, 'jpg', sep='.'), 
         plot = p, width = 10, height = p_height,
         dpi = 300)
  
  
  
  density_line <- ggplot(plot_data, aes(start,variantCount)) + 
    geom_line(aes(colour = variantCount),show.legend = FALSE) + facet_grid(chrom ~ .) + 
    theme(text = element_text(size=8)) + scale_x_continuous(expand = c(0, 0)) +
    xlab("Chromosome position") + ylab("Number of variants of each window")
  ggsave(density_line,filename = paste(output_prefix, 'line', 'jpg', sep='.'),width = 8,height = chrom_num * 0.5)
  
  density_point <- ggplot(plot_data, aes(start,variantCount)) + 
    geom_point(aes(colour = variantCount),size = 0.6,show.legend = FALSE) + 
    scale_x_continuous(expand = c(0,0))  + 
    xlab("Chromosome position") + ylab("Number of variants of each window") +
    facet_grid(chrom ~ .) + theme(text = element_text(size=8))
  ggsave(density_point,filename = paste(output_prefix, 'point', 'jpg', sep='.'),width = 8,height = chrom_num * 0.5)
  
  wrap_count = chrom_num / 3
  
  density_line_wrap <- ggplot(plot_data, aes(start,variantCount)) + 
    geom_line(aes(colour = variantCount),show.legend = FALSE) + scale_x_discrete("")+
    facet_wrap(nrow =wrap_count ,chrom ~ .) + theme(text = element_text(size=10))  + 
    xlab("Chromosome position") + ylab("Number of variants of each window")
  ggsave(density_line_wrap,filename = paste(output_prefix, 'line.wrap', 'jpg', sep='.'),width = 4,height = wrap_count)
  
  density_point_wrap <- ggplot(plot_data, aes(start,variantCount)) + 
    geom_point(aes(colour = variantCount),size = 0.6,show.legend = FALSE) + scale_x_discrete("")+
    facet_wrap(nrow =wrap_count ,chrom ~ .) + theme(text = element_text(size=10))  + 
    xlab("Chromosome position") + ylab("Number of variants of each window")
  ggsave(density_point_wrap,filename = paste(output_prefix, 'point.wrap', 'jpg', sep='.'),width = 4,height = wrap_count)
  
  density_point_oneline <- ggplot(plot_data, aes(start,variantCount)) + 
    geom_point(aes(colour = variantCount),size = 0.68,show.legend = FALSE) + scale_x_discrete("")+
    facet_grid( ~ chrom) + theme(text = element_text(size=10))  + 
    xlab("Chromosome position")+ ylab("Number of variants of each window")
  ggsave(density_point_oneline, filename = paste(output_prefix, 'point.oneline', 'jpg', sep='.'),width = chrom_num * 0.5,height = 3)
}

drawMulti <- function(plot_data, out_prefix){
  mega_base = floor(log10(max(plot_data$end)))
  mega_unit = str_pad('M', mega_base - 6 + 1,  pad = "0")
  max_chr_len = ceiling(max(plot_data$end)/(10^mega_base))
  
  cor_plot_col <- rev(colorRampPalette(brewer.pal(11, 'RdYlGn'))(100))
  
  genome_names <- unique(plot_data$genome)
  genome_num <- length(genome_names)
  
  
  plot_label <- seq(2,5*genome_num -4 + 2,5)
  plot_pos <- seq(genome_num)
  
  names(plot_label) <- genome_names
  names(plot_pos) <- genome_names
  names(genome_names) <- plot_label
  
  plot_data$y_pos <- plot_pos[plot_data$genome]
  plot_data$variantCount2 <- sapply(plot_data$variantCount, replace_zero)
  
  p <- ggplot(plot_data) + 
    geom_rect(aes(xmin=start, xmax=end, ymin=y_pos*5-5,
                  ymax=y_pos*5-1, fill = variantCount2)) +
    facet_grid(chrom~.) +
    theme(strip.text.y = element_text(size=rel(.8), 
                                      face="bold",
                                      angle = 0),
          axis.ticks = element_blank(),
          panel.background = element_rect(fill = "white"),
          axis.text.y = element_text(size=rel(0.5), margin = margin(r=-35)),
          axis.text.x = element_text(angle = 90, hjust = 1, size=rel(0.6))) +
    scale_fill_gradientn(colours = cor_plot_col) +
    xlab('') + ylab('') +
    scale_y_continuous(labels=genome_names, breaks = plot_label) +
    scale_x_continuous(limits = c(0, max_chr_len * 10^mega_base), 
                     breaks = seq(0, max_chr_len * 10^mega_base, 10^mega_base),
                     labels = c(0, paste0(seq(1, max_chr_len), mega_unit, sep = ""))) +
    guides(fill=guide_colourbar(title='Number of SNP')) 
  
  chrom_list <- as.character(unique(plot_data$chrom))
  chrom_num <- length(chrom_list)
  genome_num_scale = ifelse(genome_num < 2, 2, genome_num * 0.8)
  p_height = chrom_num * genome_num_scale / 7
  if (p_height <= 50){
    ggsave(paste(out_prefix, 'jpg', sep='.'),
           plot = p, width = 12, height = p_height,
           dpi = 300, type = "cairo")
  }
  
}

cores=detectCores()
cl <- makeCluster(cores[1] / 2)
registerDoParallel(cl)

raw_data <- fread(stats_table)
raw_data$chrom <- str_remove(raw_data$chrom, fixed('chr', ignore_case = T))


if (!'variantCount' %in% colnames(raw_data)) {
  melt_data <- melt(raw_data, id.vars = colnames(raw_data)[1:3], variable.name = 'genome', value.name = 'variantCount')
  melt_data <- melt_data[ !is.na(melt_data$variantCount) ,]
  foreach (genome = unique(melt_data$genome), .packages = c('stringr', 'ggplot2')) %dopar% {
    genome_df <- melt_data[melt_data$genome == genome,]
    out_dir = dirname(output_prefix)
    filename <- basename(output_prefix)
    genome_path = file.path(out_dir, genome)
    dir.create(genome_path)
    real_prefix <- file.path(genome_path, filename)
    drawOne(genome_df, real_prefix)
  }
  stopCluster(cl)
  drawMulti(melt_data, output_prefix)
} else {
  drawOne(raw_data, output_prefix)
}




