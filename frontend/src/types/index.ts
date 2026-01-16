/**
 * TypeScript interfaces for the Auction application data models.
 * These mirror the Django backend models.
 */

/** Minimal user information for embedding in other objects */
export interface UserMinimal {
  id: number;
  username: string;
  profile_image: string | null;
}

/** Full user profile */
export interface User extends UserMinimal {
  email: string;
  date_of_birth: string | null;
}

/** Auction item */
export interface Item {
  id: number;
  title: string;
  description: string;
  starting_price: string;
  current_price: string;
  image: string | null;
  end_datetime: string;
  owner: UserMinimal;
  bid_count: number;
  is_active: boolean;
  created_at: string;
}

/** Item with full details (for detail page) */
export interface ItemDetail extends Item {
  bids: Bid[];
  questions: Question[];
  highest_bidder: UserMinimal | null;
}

/** A bid on an auction item */
export interface Bid {
  id: number;
  item_id: number;
  bidder: UserMinimal;
  amount: string;
  timestamp: string;
}

/** An answer to a question */
export interface Answer {
  id: number;
  question_id: number;
  responder: UserMinimal;
  text: string;
  timestamp: string;
}

/** A question about an item */
export interface Question {
  id: number;
  item_id: number;
  asker: UserMinimal;
  text: string;
  timestamp: string;
  answers: Answer[];
}

/** API response for items list */
export interface ItemsResponse {
  items: Item[];
  count: number;
}

/** API response for bids list */
export interface BidsResponse {
  bids: Bid[];
  count: number;
}

/** API response for questions list */
export interface QuestionsResponse {
  questions: Question[];
  count: number;
}

/** API response for user status */
export interface UserStatusResponse {
  authenticated: boolean;
  user: User;
}

/** Form data for creating a new item */
export interface CreateItemForm {
  title: string;
  description: string;
  starting_price: string;
  end_datetime: string;
  image: File | null;
}

/** Form data for updating profile */
export interface UpdateProfileForm {
  email?: string;
  date_of_birth?: string;
  profile_image?: File;
}

/** Form data for placing a bid */
export interface PlaceBidForm {
  amount: string;
}

/** Form data for asking/answering questions */
export interface QuestionForm {
  text: string;
}

/** Generic API error response */
export interface ApiError {
  error: string;
}
