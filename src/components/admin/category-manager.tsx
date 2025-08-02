"use client";

import * as React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { categories as initialCategories } from "@/lib/data";
import { Edit, Trash2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export function CategoryManager() {
  const [categories, setCategories] = React.useState(initialCategories);
  const [isDialogOpen, setIsDialogOpen] = React.useState(false);
  const [currentCategory, setCurrentCategory] = React.useState<string | null>(null);
  const [newCategoryName, setNewCategoryName] = React.useState("");
  const { toast } = useToast();

  const handleOpenDialog = (category?: string) => {
    setCurrentCategory(category || null);
    setNewCategoryName(category || "");
    setIsDialogOpen(true);
  };

  const handleSaveCategory = () => {
    if (!newCategoryName.trim()) {
        toast({ title: "Error", description: "Category name cannot be empty.", variant: "destructive"});
        return;
    }

    if (currentCategory) { // Editing
      setCategories(categories.map(c => c === currentCategory ? newCategoryName : c));
      toast({ title: "Success", description: "Category updated."});
    } else { // Adding
      if (categories.includes(newCategoryName)) {
        toast({ title: "Error", description: "Category already exists.", variant: "destructive"});
        return;
      }
      setCategories([...categories, newCategoryName]);
      toast({ title: "Success", description: "Category added."});
    }
    setIsDialogOpen(false);
    setNewCategoryName("");
    setCurrentCategory(null);
  };
  
  const handleDeleteCategory = (category: string) => {
    setCategories(categories.filter(c => c !== category));
    toast({ title: "Success", description: "Category deleted."});
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Manage Categories</CardTitle>
        <Button onClick={() => handleOpenDialog()}>Add New Category</Button>
      </CardHeader>
      <CardContent>
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Category Name</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {categories.map((category) => (
                <TableRow key={category}>
                  <TableCell className="font-medium">{category}</TableCell>
                  <TableCell className="text-right space-x-2">
                    <Button variant="ghost" size="icon" onClick={() => handleOpenDialog(category)}>
                        <Edit className="h-4 w-4" />
                    </Button>
                     <Button variant="ghost" size="icon" onClick={() => handleDeleteCategory(category)}>
                        <Trash2 className="h-4 w-4 text-destructive" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>{currentCategory ? "Edit" : "Add"} Category</DialogTitle>
              <DialogDescription>
                {currentCategory ? "Update the name of this category." : "Create a new category for support tickets."}
              </DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="name" className="text-right">Name</Label>
                    <Input id="name" value={newCategoryName} onChange={(e) => setNewCategoryName(e.target.value)} className="col-span-3" />
                </div>
            </div>
            <DialogFooter>
                <Button variant="outline" onClick={() => setIsDialogOpen(false)}>Cancel</Button>
                <Button onClick={handleSaveCategory}>Save</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </CardContent>
    </Card>
  );
}
