module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "task-tracker"
  cluster_version = "1.29"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    default = {
      desired_size = 2
      instance_types = ["t3.medium"]
    }
  }
}
