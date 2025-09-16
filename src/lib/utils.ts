import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function getAgeBasedTier(age: number): 'magic_workshop' | 'innovation_lab' | 'professional_studio' {
  if (age >= 5 && age <= 7) return 'magic_workshop'
  if (age >= 8 && age <= 9) return 'innovation_lab'
  return 'professional_studio'
}

export function getTierDisplayName(tier: string): string {
  switch (tier) {
    case 'magic_workshop':
      return 'Magic Workshop'
    case 'innovation_lab':
      return 'Innovation Lab'
    case 'professional_studio':
      return 'Professional Studio'
    default:
      return 'Unknown Tier'
  }
}

export function getTierDescription(tier: string): string {
  switch (tier) {
    case 'magic_workshop':
      return 'Where coding feels like casting spells with Sparkle the Unicorn'
    case 'innovation_lab':
      return 'Build real apps and games with Robo the Robot'
    case 'professional_studio':
      return 'Real coding languages and professional tools with CodeMentor AI'
    default:
      return 'Discover your coding journey'
  }
}

export function getTierAgeRange(tier: string): string {
  switch (tier) {
    case 'magic_workshop':
      return 'Ages 5-7'
    case 'innovation_lab':
      return 'Ages 8-9'
    case 'professional_studio':
      return 'Ages 10+'
    default:
      return 'All Ages'
  }
}

